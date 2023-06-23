from __future__ import annotations
import re
import os


class Alert:
    def __init__(self, lines=[]) -> None:
        self.from_lines(lines)

    def from_lines(self, lines):
        splitted = [t.strip() for t in lines]
        self.lines = [t for t in splitted if len(t) > 0]
        return self

    def from_toot(self, toot_content):
        stripped = toot_content.replace("<p>", "").replace("</p>", "").strip()
        splitted = [t for t in stripped.split("<br />")]
        return self.from_lines(splitted)

    def is_same(self, other: Alert):
        # TODO: optimize directly from lines
        return self.text() == other.text()

    def is_in_list(self, list_of_alerts: list[Alert]):
        # TODO: optimize directly from lines
        return any(self.text() == a.text() for a in list_of_alerts)

    def text(self):
        return "\n".join(self.lines).strip()

    def places(self):
        places = [t for t in self.lines if not Alert.reg_date.match(t)]
        places = [t for t in places if all(p not in t for p in Alert.non_places)]
        places = [Alert.reg_paranthesis.sub("", t).strip() for t in places]
        return places

    def show_places(self):
        return str(Alert.reverse_if_needed(self.places()))

    def show(self, also_places=False):
        """concat lines and reverse each line since hebrew is not shown well"""
        return " ".join(Alert.reverse_if_needed(self.lines))

    @staticmethod
    def reverse_if_needed(parts):
        if Alert.need_heb_rev:
            return [p if re.search("[א-ת]", p) is None else "".join(reversed(p)) for p in parts]
        else:
            return parts

    non_places = ["ירי רקטות וטילים", "היכנסו למרחב המוגן"]
    reg_date = re.compile("^[0-9:\- ]+$")
    reg_paranthesis = re.compile("\([^)]*\)")
    need_heb_rev = "TERM_PROGRAM" in os.environ.keys() and os.environ["TERM_PROGRAM"] == "vscode"
