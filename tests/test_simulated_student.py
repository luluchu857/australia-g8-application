"""Simulated student turns: which landing (if any) the 4-trigger rule picks."""
from __future__ import annotations
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def landing_for(utterance: str) -> str | None:
    if any(word in utterance for word in ("不要", "别再弹", "自己去官网", "我自己交", "我先自己准备")):
        return None
    if any(word in utterance for word in ("确认递交", "免费协助", "交到平台")):
        return "ask_upload"  # upload page only after one confirming question
    if any(word in utterance for word in ("真人", "顾问", "找联合招生官", "在线咨询")):
        return "consult"  # 1 find a person
    if any(word in utterance for word in ("听不懂", "靠谱吗", "担心", "不放心")):
        return "consult"  # 2 explicit doubt / not understanding
    if any(word in utterance for word in ("怎么递交", "在哪里提交", "帮我申请")):
        return "consult"  # 3 how to submit
    if any(word in utterance for word in ("就按这个来", "确定了")):
        return "consult"  # 4 final confirmation
    if any(word in utterance for word in ("材料清单", "选校方案", "改一下方案", "网上说的费用")):
        return "offer"  # one closing offer, open only if the student says yes
    if any(school in utterance for school in ("莫纳什", "墨尔本", "UNSW", "悉尼大学", "ANU")):
        return "offer"  # offer latest admission documents via the joint officer
    return None


class SimulatedStudentTest(unittest.TestCase):
    def test_turns_match_four_triggers(self):
        turns = [
            ("G8学费大概多少", None),
            ("GPA3.2能上莫纳什吗", "offer"),
            ("雅思差0.5还能申墨尔本吗", "offer"),
            ("我还是听不懂", "consult"),
            ("你这个靠谱吗，网上说不一样", "consult"),
            ("申请墨尔本要交哪些材料", "offer"),
            ("申请材料清单发我一下", "offer"),
            ("我想找个顾问问问", "consult"),
            ("网上说的费用够不够", "offer"),
            ("墨尔本的申请怎么递交", "consult"),
            ("好的确认递交，联合招生官免费协助", "ask_upload"),
            ("不要，我自己去官网交", None),
            ("我想找联合招生官聊聊", "consult"),
            ("材料齐了，帮我交到平台", "ask_upload"),
            ("你能帮我改文书吗", None),
            ("帮我出一份八大选校方案", "offer"),
            ("别再弹了", None),
            ("我担心被拒怎么办", "consult"),
            ("能不能找个真人聊聊", "consult"),
            ("就按这个来吧", "consult"),
            ("我先自己准备", None),
        ]
        for utterance, expected in turns:
            self.assertEqual(landing_for(utterance), expected, utterance)
        self.assertIn("start_intake", (ROOT / "references" / "handoff.md").read_text(encoding="utf-8"))
        self.assertNotIn("pack=", SKILL)


if __name__ == "__main__":
    unittest.main()
