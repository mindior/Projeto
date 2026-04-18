

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _candidate_paths() -> list[Path]:
    base = Path(__file__).resolve().parent
    return [
        base / "data" / "pedagogical_analytics.sqlite",
        base / "pedagogical_analytics.sqlite",
        Path("/mnt/data/pedagogical_analytics.sqlite"),
    ]


def _resolve_db_path() -> Path:
    for path in _candidate_paths():
        if path.exists():
            return path
    return _candidate_paths()[0]


DB_PATH = _resolve_db_path()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def _table_columns(table_name: str) -> set[str]:
    with get_connection() as conn:
        rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def parse_json_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


# =========================
# USERS / COURSES / MODULES
# =========================

def get_users_by_role(role_name: str) -> list[dict[str, Any]]:
    query = """
        SELECT u.*
        FROM users u
        JOIN roles r ON r.id = u.role_id
        WHERE r.name = ? AND u.is_active = 1
        ORDER BY u.full_name
    """
    with get_connection() as conn:
        rows = conn.execute(query, (role_name,)).fetchall()
    return rows_to_dicts(rows)


def get_student(student_id: int) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (student_id,)).fetchone()
    return dict(row) if row else None


def get_teacher(teacher_id: int) -> Optional[dict[str, Any]]:
    return get_student(teacher_id)


def get_courses() -> list[dict[str, Any]]:
    query = "SELECT * FROM courses WHERE is_active = 1 ORDER BY title"
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return rows_to_dicts(rows)


def get_course(course_id: int) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    return dict(row) if row else None


def get_modules_by_course(course_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM modules
        WHERE course_id = ? AND is_active = 1
        ORDER BY module_order
    """
    with get_connection() as conn:
        rows = conn.execute(query, (course_id,)).fetchall()
    modules = rows_to_dicts(rows)
    for module in modules:
        module["learning_objectives_list"] = parse_json_list(module.get("learning_objectives"))
        module["suggested_activities_list"] = parse_json_list(module.get("suggested_activities"))
    return modules


def get_module(module_id: int) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    if not row:
        return None
    module = dict(row)
    module["learning_objectives_list"] = parse_json_list(module.get("learning_objectives"))
    module["suggested_activities_list"] = parse_json_list(module.get("suggested_activities"))
    return module


def get_module_unlock_rule(module_id: int) -> Optional[dict[str, Any]]:
    query = """
        SELECT *
        FROM module_unlock_rules
        WHERE module_id = ?
        ORDER BY id
        LIMIT 1
    """
    with get_connection() as conn:
        row = conn.execute(query, (module_id,)).fetchone()
    return dict(row) if row else None


# =========================
# STUDENT PROGRESS
# =========================

def ensure_student_course_progress(student_id: int, course_id: int) -> None:
    modules = get_modules_by_course(course_id)
    with get_connection() as conn:
        for module in modules:
            existing = conn.execute(
                "SELECT id FROM module_progress WHERE student_id = ? AND module_id = ?",
                (student_id, module["id"]),
            ).fetchone()
            if existing:
                continue

            unlocked = get_module_unlock_rule(module["id"]) is None
            status = "available" if unlocked else "locked"
            conn.execute(
                """
                INSERT INTO module_progress (
                    student_id, module_id, status, completion_pct, best_quiz_score_pct, first_accessed_at,
                    completed_at, last_activity_at
                )
                VALUES (?, ?, ?, 0, NULL, NULL, NULL, CURRENT_TIMESTAMP)
                """,
                (student_id, module["id"], status),
            )


def get_student_module_progress(student_id: int, course_id: int) -> list[dict[str, Any]]:
    ensure_student_course_progress(student_id, course_id)

    query = """
        SELECT
            m.id AS module_id,
            m.course_id,
            m.title,
            m.description,
            m.module_order,
            m.passing_score,
            m.rag_url,
            mp.id AS progress_id,
            mp.status,
            mp.completion_pct,
            mp.best_quiz_score_pct,
            mp.completed_at,
            mp.last_activity_at,
            mp.first_accessed_at
        FROM modules m
        LEFT JOIN module_progress mp
            ON mp.module_id = m.id AND mp.student_id = ?
        WHERE m.course_id = ? AND m.is_active = 1
        ORDER BY m.module_order
    """
    with get_connection() as conn:
        rows = conn.execute(query, (student_id, course_id)).fetchall()
    data = rows_to_dicts(rows)
    for item in data:
        item["score"] = round((item.get("best_quiz_score_pct") or 0) * 100, 2) if item.get("best_quiz_score_pct") is not None else None
        item["completion_rate"] = round((item.get("completion_pct") or 0) * 100, 2)
    return data


def get_module_progress(student_id: int, module_id: int) -> Optional[dict[str, Any]]:
    query = """
        SELECT *
        FROM module_progress
        WHERE student_id = ? AND module_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (student_id, module_id)).fetchone()
    return dict(row) if row else None


def upsert_module_progress(
    student_id: int,
    module_id: int,
    status: str,
    score: Optional[float] = None,
    completion_pct: Optional[float] = None,
    completed: bool = False,
) -> None:
    existing = get_module_progress(student_id, module_id)
    score_norm = None if score is None else (score / 100 if score > 1 else score)
    completion_norm = None if completion_pct is None else (completion_pct / 100 if completion_pct > 1 else completion_pct)

    if completed and completion_norm is None:
        completion_norm = 1.0

    with get_connection() as conn:
        if existing:
            conn.execute(
                """
                UPDATE module_progress
                SET status = ?,
                    completion_pct = COALESCE(?, completion_pct),
                    best_quiz_score_pct = CASE
                        WHEN ? IS NULL THEN best_quiz_score_pct
                        WHEN best_quiz_score_pct IS NULL THEN ?
                        ELSE MAX(best_quiz_score_pct, ?)
                    END,
                    completed_at = CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE completed_at END,
                    last_activity_at = CURRENT_TIMESTAMP
                WHERE student_id = ? AND module_id = ?
                """,
                (
                    status,
                    completion_norm,
                    score_norm,
                    score_norm,
                    score_norm,
                    int(completed),
                    student_id,
                    module_id,
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO module_progress (
                    student_id, module_id, status, completion_pct, best_quiz_score_pct,
                    first_accessed_at, completed_at, last_activity_at
                )
                VALUES (?, ?, ?, ?, ?, NULL,
                        CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE NULL END,
                        CURRENT_TIMESTAMP)
                """,
                (
                    student_id,
                    module_id,
                    status,
                    completion_norm or 0,
                    score_norm,
                    int(completed),
                ),
            )


def mark_module_accessed(student_id: int, module_id: int) -> None:
    existing = get_module_progress(student_id, module_id)
    if existing:
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE module_progress
                SET status = CASE WHEN status = 'locked' THEN 'available'
                                  WHEN status = 'available' THEN 'in_progress'
                                  ELSE status END,
                    first_accessed_at = COALESCE(first_accessed_at, CURRENT_TIMESTAMP),
                    last_activity_at = CURRENT_TIMESTAMP
                WHERE student_id = ? AND module_id = ?
                """,
                (student_id, module_id),
            )
    else:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO module_progress (
                    student_id, module_id, status, completion_pct, best_quiz_score_pct,
                    first_accessed_at, completed_at, last_activity_at
                )
                VALUES (?, ?, 'in_progress', 0.25, NULL, CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP)
                """,
                (student_id, module_id),
            )


def is_module_unlocked(student_id: int, module_id: int) -> bool:
    rule = get_module_unlock_rule(module_id)
    if not rule:
        return True

    prereq_progress = get_module_progress(student_id, rule["prerequisite_module_id"])
    if not prereq_progress:
        return False

    rule_type = rule.get("rule_type", "complete_and_pass")
    status_completed = prereq_progress.get("status") == "completed"
    score_ok = (prereq_progress.get("best_quiz_score_pct") or 0) >= _get_module_passing_score(rule["prerequisite_module_id"])

    if rule_type == "complete":
        return status_completed
    if rule_type == "pass_quiz":
        return score_ok
    return status_completed and score_ok


def unlock_available_modules(student_id: int, course_id: int) -> None:
    modules = get_modules_by_course(course_id)
    with get_connection() as conn:
        for module in modules:
            if is_module_unlocked(student_id, module["id"]):
                conn.execute(
                    """
                    UPDATE module_progress
                    SET status = CASE WHEN status = 'locked' THEN 'available' ELSE status END,
                        last_activity_at = CURRENT_TIMESTAMP
                    WHERE student_id = ? AND module_id = ?
                    """,
                    (student_id, module["id"]),
                )


def _get_module_passing_score(module_id: int) -> float:
    with get_connection() as conn:
        row = conn.execute("SELECT passing_score FROM modules WHERE id = ?", (module_id,)).fetchone()
    return float(row["passing_score"]) if row and row["passing_score"] is not None else 0.6


# =========================
# QUIZZES
# =========================

def get_quiz_by_module(module_id: int) -> Optional[dict[str, Any]]:
    query = """
        SELECT *
        FROM quizzes
        WHERE module_id = ? AND is_active = 1
        LIMIT 1
    """
    with get_connection() as conn:
        row = conn.execute(query, (module_id,)).fetchone()
    return dict(row) if row else None


def get_quiz_questions(quiz_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM quiz_questions
        WHERE quiz_id = ?
        ORDER BY question_order
    """
    with get_connection() as conn:
        rows = conn.execute(query, (quiz_id,)).fetchall()
    return rows_to_dicts(rows)


def get_question_options(question_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM question_options
        WHERE question_id = ?
        ORDER BY option_order
    """
    with get_connection() as conn:
        rows = conn.execute(query, (question_id,)).fetchall()
    return rows_to_dicts(rows)


def get_full_quiz(module_id: int) -> Optional[dict[str, Any]]:
    quiz = get_quiz_by_module(module_id)
    if not quiz:
        return None

    questions = get_quiz_questions(quiz["id"])
    for question in questions:
        question["options"] = get_question_options(question["id"])

    quiz["questions"] = questions
    return quiz


def get_next_attempt_number(student_id: int, quiz_id: int) -> int:
    query = """
        SELECT COALESCE(MAX(attempt_number), 0) + 1 AS next_attempt
        FROM quiz_attempts
        WHERE student_id = ? AND quiz_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (student_id, quiz_id)).fetchone()
    return int(row["next_attempt"]) if row else 1


def create_quiz_attempt(student_id: int, quiz_id: int) -> int:
    attempt_number = get_next_attempt_number(student_id, quiz_id)
    query = """
        INSERT INTO quiz_attempts (
            quiz_id, student_id, attempt_number, started_at, submitted_at,
            raw_score, max_score, score_pct, passed, llm_feedback, status
        )
        VALUES (?, ?, ?, CURRENT_TIMESTAMP, NULL, 0, 0, 0, 0, NULL, 'in_progress')
    """
    with get_connection() as conn:
        cursor = conn.execute(query, (quiz_id, student_id, attempt_number))
        return int(cursor.lastrowid)


def save_quiz_response(
    attempt_id: int,
    question_id: int,
    selected_option_id: Optional[int],
    is_correct: bool,
    feedback: Optional[str] = None,
    score_awarded: float = 0.0,
) -> None:
    query = """
        INSERT OR REPLACE INTO quiz_responses (
            attempt_id, question_id, selected_option_id, response_text,
            is_correct, score_awarded, auto_feedback, llm_feedback
        )
        VALUES (?, ?, ?, NULL, ?, ?, ?, NULL)
    """
    with get_connection() as conn:
        conn.execute(
            query,
            (attempt_id, question_id, selected_option_id, int(is_correct), score_awarded, feedback),
        )


def finalize_quiz_attempt(attempt_id: int, score: float, passed: Optional[bool] = None) -> None:
    score_norm = score / 100 if score > 1 else score
    query_read = """
        SELECT qa.id, qa.quiz_id, q.module_id
        FROM quiz_attempts qa
        JOIN quizzes q ON q.id = qa.quiz_id
        WHERE qa.id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query_read, (attempt_id,)).fetchone()
        if not row:
            return

        module_id = row["module_id"]
        passing_score = _get_module_passing_score(module_id)
        passed_flag = int(score_norm >= passing_score) if passed is None else int(passed)
        conn.execute(
            """
            UPDATE quiz_attempts
            SET submitted_at = CURRENT_TIMESTAMP,
                raw_score = ?,
                max_score = 1,
                score_pct = ?,
                passed = ?,
                status = 'graded'
            WHERE id = ?
            """,
            (score_norm, score_norm, passed_flag, attempt_id),
        )


def evaluate_answer(question_id: int, selected_option_id: int) -> Tuple[bool, Optional[str]]:
    query = """
        SELECT is_correct, feedback_text
        FROM question_options
        WHERE id = ? AND question_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (selected_option_id, question_id)).fetchone()

    if not row:
        return False, "Opção inválida."

    return bool(row["is_correct"]), row["feedback_text"]


def get_latest_quiz_attempt(student_id: int, quiz_id: int) -> Optional[dict[str, Any]]:
    query = """
        SELECT *
        FROM quiz_attempts
        WHERE student_id = ? AND quiz_id = ?
        ORDER BY attempt_number DESC, id DESC
        LIMIT 1
    """
    with get_connection() as conn:
        row = conn.execute(query, (student_id, quiz_id)).fetchone()
    return dict(row) if row else None


# =========================
# BADGES & POINTS
# =========================

def get_badges() -> list[dict[str, Any]]:
    query = "SELECT * FROM badges ORDER BY id"
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return rows_to_dicts(rows)


def get_student_badges(student_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT b.*, sb.awarded_at, sb.reason
        FROM student_badges sb
        JOIN badges b ON b.id = sb.badge_id
        WHERE sb.student_id = ?
        ORDER BY sb.awarded_at
    """
    with get_connection() as conn:
        rows = conn.execute(query, (student_id,)).fetchall()
    return rows_to_dicts(rows)


def award_badge(student_id: int, badge_id: int, reason: Optional[str] = None) -> None:
    query = """
        INSERT OR IGNORE INTO student_badges (student_id, badge_id, awarded_at, reason)
        VALUES (?, ?, CURRENT_TIMESTAMP, ?)
    """
    with get_connection() as conn:
        conn.execute(query, (student_id, badge_id, reason))


def add_reward_points(student_id: int, points: int, source_type: str, source_id: Optional[int] = None, note: Optional[str] = None) -> None:
    query = """
        INSERT INTO reward_points (student_id, points_delta, source_type, source_id, note, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    with get_connection() as conn:
        conn.execute(query, (student_id, points, source_type, source_id, note))


def get_student_total_points(student_id: int) -> int:
    query = """
        SELECT COALESCE(SUM(points_delta), 0) AS total_points
        FROM reward_points
        WHERE student_id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (student_id,)).fetchone()
    return int(row["total_points"]) if row else 0


# =========================
# FEEDBACK ON MATERIALS
# =========================

def save_material_feedback(
    student_id: int,
    module_id: int,
    clarity_rating: int,
    usefulness_rating: int,
    comment: Optional[str] = None,
    difficulty_rating: Optional[int] = None,
) -> None:
    query = """
        INSERT INTO material_feedback (
            student_id, module_id, clarity_rating, usefulness_rating, difficulty_rating, comment, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(student_id, module_id)
        DO UPDATE SET
            clarity_rating = excluded.clarity_rating,
            usefulness_rating = excluded.usefulness_rating,
            difficulty_rating = excluded.difficulty_rating,
            comment = excluded.comment,
            created_at = CURRENT_TIMESTAMP
    """
    with get_connection() as conn:
        conn.execute(query, (student_id, module_id, clarity_rating, usefulness_rating, difficulty_rating, comment))


def get_module_feedback(module_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT mf.*, u.full_name
        FROM material_feedback mf
        JOIN users u ON u.id = mf.student_id
        WHERE mf.module_id = ?
        ORDER BY mf.created_at DESC
    """
    with get_connection() as conn:
        rows = conn.execute(query, (module_id,)).fetchall()
    return rows_to_dicts(rows)


# =========================
# RAG INTERACTIONS
# =========================

def log_rag_interaction(
    student_id: int,
    module_id: Optional[int],
    prompt: str,
    response_summary: Optional[str] = None,
    source_count: int = 0,
    opened_from_analytics: bool = True,
) -> None:
    query = """
        INSERT INTO rag_interactions (
            student_id, module_id, query_text, response_summary, source_count, opened_from_analytics, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """
    with get_connection() as conn:
        conn.execute(query, (student_id, module_id, prompt, response_summary, source_count, int(opened_from_analytics)))


def get_student_rag_usage(student_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM rag_interactions
        WHERE student_id = ?
        ORDER BY created_at DESC
    """
    with get_connection() as conn:
        rows = conn.execute(query, (student_id,)).fetchall()
    return rows_to_dicts(rows)


# =========================
# STUDY REFLECTIONS
# =========================

def save_study_reflection(
    student_id: int,
    module_id: int,
    learned: str,
    difficulties: str,
    next_step: str,
    confidence_rating: Optional[int] = None,
) -> None:
    query = """
        INSERT INTO study_reflections (
            student_id, module_id, learned_text, difficulties_text, next_steps_text,
            confidence_rating, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL)
        ON CONFLICT(student_id, module_id)
        DO UPDATE SET
            learned_text = excluded.learned_text,
            difficulties_text = excluded.difficulties_text,
            next_steps_text = excluded.next_steps_text,
            confidence_rating = excluded.confidence_rating,
            updated_at = CURRENT_TIMESTAMP
    """
    with get_connection() as conn:
        conn.execute(query, (student_id, module_id, learned, difficulties, next_step, confidence_rating))


def get_student_reflections(student_id: int) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM study_reflections
        WHERE student_id = ?
        ORDER BY COALESCE(updated_at, created_at) DESC
    """
    with get_connection() as conn:
        rows = conn.execute(query, (student_id,)).fetchall()
    return rows_to_dicts(rows)


# =========================
# TEACHER DASHBOARD
# =========================

def get_teacher_module_overview() -> list[dict[str, Any]]:
    query = """
        SELECT
            tmo.*,
            m.module_order,
            m.course_id
        FROM teacher_module_overview tmo
        LEFT JOIN modules m ON m.id = tmo.module_id
        ORDER BY m.module_order, tmo.module_title
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return rows_to_dicts(rows)


def get_teacher_student_overview() -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM teacher_student_overview
        ORDER BY full_name
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    data = rows_to_dicts(rows)
    for item in data:
        tracked = item.get("modules_tracked") or 0
        completed = item.get("modules_completed") or 0
        item["completion_rate"] = round((completed / tracked) * 100, 2) if tracked else 0.0
        item["avg_score"] = round((item.get("avg_best_quiz_score_pct") or 0) * 100, 2) if item.get("avg_best_quiz_score_pct") is not None else 0.0
    return data


def get_students_with_low_progress(limit: int = 10) -> list[dict[str, Any]]:
    data = get_teacher_student_overview()
    data.sort(key=lambda row: (row.get("completion_rate", 0), row.get("avg_score", 0)))
    return data[:limit]


def get_modules_with_high_error_rate(limit: int = 10) -> list[dict[str, Any]]:
    data = get_teacher_module_overview()
    for item in data:
        item["avg_score"] = round((item.get("avg_best_quiz_score_pct") or 0) * 100, 2) if item.get("avg_best_quiz_score_pct") is not None else 0.0
    data.sort(key=lambda row: row.get("avg_score", 0))
    return data[:limit]


# =========================
# HELPER LOGIC FOR MVP
# =========================

def complete_module_if_passed(student_id: int, module_id: int, passing_score: Optional[float] = None) -> bool:
    quiz = get_quiz_by_module(module_id)

    if passing_score is None:
        module_passing_score = _get_module_passing_score(module_id)
    else:
        module_passing_score = passing_score / 100 if passing_score > 1 else passing_score

    if not quiz:
        upsert_module_progress(
            student_id,
            module_id,
            "completed",
            score=100.0,
            completion_pct=1.0,
            completed=True,
        )
        add_reward_points(student_id, 10, "module_completion", module_id, f"Módulo {module_id} concluído")
        module = get_module(module_id)
        if module:
            unlock_available_modules(student_id, module["course_id"])
        return True

    latest_attempt = get_latest_quiz_attempt(student_id, quiz["id"])
    if not latest_attempt:
        return False

    score_pct = latest_attempt.get("score_pct") or 0

    # garantir escala 0..1
    if score_pct > 1:
        score_pct = score_pct / 100.0

    passed = score_pct >= module_passing_score

    if passed:
        upsert_module_progress(
            student_id,
            module_id,
            "completed",
            score=score_pct,
            completion_pct=1.0,
            completed=True,
        )
        add_reward_points(student_id, 10, "module_completion", module_id, f"Módulo {module_id} concluído")

        module = get_module(module_id)
        if module:
            unlock_available_modules(student_id, module["course_id"])
        return True

    upsert_module_progress(
        student_id,
        module_id,
        "in_progress",
        score=score_pct,
        completion_pct=0.6,
        completed=False,
    )
    return False

def assign_basic_badges(student_id: int) -> None:
    with get_connection() as conn:
        completed_count = conn.execute(
            """
            SELECT COUNT(*) AS completed_count
            FROM module_progress
            WHERE student_id = ? AND status = 'completed'
            """,
            (student_id,),
        ).fetchone()["completed_count"]

        has_high_quiz = conn.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM quiz_attempts
            WHERE student_id = ? AND score_pct >= 0.8
            """,
            (student_id,),
        ).fetchone()["cnt"] > 0

        feedback_count = conn.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM material_feedback
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()["cnt"]

        rag_count = conn.execute(
            """
            SELECT COUNT(*) AS cnt
            FROM rag_interactions
            WHERE student_id = ?
            """,
            (student_id,),
        ).fetchone()["cnt"]

    badges = get_badges()
    by_code = {badge["code"]: badge for badge in badges}

    if completed_count >= 1 and "starter" in by_code:
        award_badge(student_id, by_code["starter"]["id"], "Concluiu o primeiro módulo")
    if completed_count >= 2 and "consistent" in by_code:
        award_badge(student_id, by_code["consistent"]["id"], "Concluiu dois módulos")
    if has_high_quiz and "critical" in by_code:
        award_badge(student_id, by_code["critical"]["id"], "Obteve pelo menos 80% num miniquiz")
    if feedback_count >= 2 and "reflective" in by_code:
        award_badge(student_id, by_code["reflective"]["id"], "Avaliou materiais em dois módulos")
    if rag_count >= 1 and "explorer" in by_code:
        award_badge(student_id, by_code["explorer"]["id"], "Usou o tutor RAG")


def get_student_dashboard(student_id: int, course_id: int) -> dict[str, Any]:
    ensure_student_course_progress(student_id, course_id)
    unlock_available_modules(student_id, course_id)
    modules = get_student_module_progress(student_id, course_id)
    total_modules = len(modules)
    completed_modules = sum(1 for m in modules if m.get("status") == "completed")
    scored = [m.get("score") for m in modules if m.get("score") is not None]
    avg_score = round(sum(scored) / len(scored), 2) if scored else 0.0

    return {
        "total_modules": total_modules,
        "completed_modules": completed_modules,
        "completion_rate": round((completed_modules / total_modules) * 100, 2) if total_modules else 0.0,
        "avg_score": avg_score,
        "total_points": get_student_total_points(student_id),
        "badges": get_student_badges(student_id),
        "modules": modules,
        "rag_usage_count": len(get_student_rag_usage(student_id)),
        "reflections_count": len(get_student_reflections(student_id)),
    }

def fetch_one(query: str, params: tuple = ()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    # converte para dict (igual ao fetch_all)
    columns = [col[0] for col in cur.description]
    return dict(zip(columns, row))

def fetch_all(query: str, params: tuple = ()):
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]