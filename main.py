import json
import os
from django.utils import timezone
from db.models import Race, Skill, Player, Guild


def main() -> None:
    json_path = os.path.join(os.path.dirname(__file__), "players.json")

    with open(json_path, "r", encoding="utf-8") as f:
        players_data = json.load(f)  # this is a dict

    for player_data in players_data.values():
        nickname = player_data.get("nickname")
        if not nickname:
            nickname = next(
                key for key, val in players_data.items() if val == player_data
            )

        # ---- Race ----
        race_data = player_data["race"]
        race, _ = Race.objects.get_or_create(
            name=race_data["name"],
            defaults={"description": race_data.get("description", "")},
        )

        # ---- Skills ----
        for skill_data in race_data.get("skills", []):
            skill, _ = Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults={"bonus": skill_data["bonus"], "race": race},
            )
            if skill.race != race:
                skill.race = race
                skill.save()

        # ---- Guild ----
        guild_data = player_data.get("guild")
        guild = None
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data["name"],
                defaults={"description": guild_data.get("description")},
            )

        # ---- Player ----
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data["email"],
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
                "created_at": timezone.now(),
            },
        )


if __name__ == "__main__":
    main()
