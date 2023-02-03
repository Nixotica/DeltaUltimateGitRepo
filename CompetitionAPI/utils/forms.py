class CompetitionBasicInfo:
    def __init__(
            self,
            name: str,
            club: str,
            teams: bool,
            desc: str = None,
            rules: str = None):
        self.name = name
        self.club = club
        self.teams = teams
        self.desc = desc
        self.rules = rules
