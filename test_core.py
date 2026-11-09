"""Unit tests (run with: python -m unittest discover tests)."""
import unittest
from src.skills import extract_skills
from src.analyzer import analyze_resume, detect_sections, contact_info
from src.matcher import load_jobs, match_jobs, match_custom_jd


class TestSkills(unittest.TestCase):
    def test_extracts_known_skills(self):
        found = extract_skills("I know Python, C++ and Node.js with Git.")
        for s in ["python", "c++", "node.js", "git"]:
            self.assertIn(s, found)

    def test_no_false_positive_for_substrings(self):
        self.assertNotIn("java", extract_skills("I like javascript only"))

    def test_empty_text(self):
        self.assertEqual(extract_skills(""), [])


class TestAnalyzer(unittest.TestCase):
    def test_sections_detected(self):
        s = detect_sections("Education\nSkills\nProjects")
        self.assertTrue(s["Education"] and s["Skills"] and s["Projects"])
        self.assertFalse(s["Certifications"])

    def test_contact_detection(self):
        c = contact_info("a@b.com 9876543210 github.com/x")
        self.assertTrue(all(c.values()))

    def test_score_bounds(self):
        r = analyze_resume("hello", [])
        self.assertTrue(0 <= r["score"] <= 100)
        self.assertTrue(len(r["tips"]) > 0)


class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.jobs = load_jobs()

    def test_ranking_is_sorted(self):
        text = "Python pandas numpy sql machine learning scikit-learn git"
        res = match_jobs(text, extract_skills(text), self.jobs)
        scores = [r["score"] for r in res]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_best_match_for_ml_profile(self):
        text = "Python machine learning deep learning tensorflow scikit-learn nlp git algorithms"
        res = match_jobs(text, extract_skills(text), self.jobs)
        self.assertEqual(res[0]["title"], "Machine Learning Engineer")

    def test_custom_jd(self):
        text = "Python Django git"
        r = match_custom_jd(text, extract_skills(text), "Need Python and Django developer")
        self.assertGreater(r["score"], 40)


if __name__ == "__main__":
    unittest.main()
