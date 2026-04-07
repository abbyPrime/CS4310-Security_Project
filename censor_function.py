from typing import List, Dict, Any

def can_view_line(
    line: Dict[str, Any],
    member: Dict[str, Any]
) -> bool:
    """
    Determine if a production member can view a script line.
    """

    # Unpack line fields
    speaker = line["character"]
    secondary_chars = line["secondary_characters"]
    scene = line["scene"]
    events = line["events"]

    # Unpack member permissions
    played_chars = member.get("characters_played", [])
    known_chars = member.get("characters_known", [])
    known_scenes = member.get("scenes_known", [])
    known_events = member.get("major_events_known", [])

    # Normalize "not applicable"
    if known_scenes == "ALL":
        known_scenes = None

    # Rule 1: If they play the speaker, allow
    if speaker in played_chars:
        return True

    # Rule 2: If scene is restricted
    if known_scenes is not None and scene not in known_scenes:
        return False

    # Rule 3: If speaker is unknown
    if speaker not in known_chars and speaker not in played_chars:
        return False

    # Rule 4: Secondary characters must be known
    for char in secondary_chars:
        if char not in known_chars and char not in played_chars:
            return False

    # Rule 5: Events must be known
    for event in events:
        if event not in known_events:
            return False

    return True


def filter_script(
    script_lines: List[str],
    script_table: List[Dict[str, Any]],
    member: Dict[str, Any]
) -> List[str]:
    """
    Returns a filtered version of the script with restricted lines redacted.
    """

    filtered_output = []

    # Map line number -> metadata
    line_lookup = {line["line_number"]: line for line in script_table}

    for raw_line in script_lines:
        try:
            # Expect format: "12: some dialogue"
            line_number = int(raw_line.split(":", 1)[0])
        except:
            # If formatting fails, keep line unchanged
            filtered_output.append(raw_line)
            continue

        if line_number not in line_lookup:
            filtered_output.append(raw_line)
            continue

        line_meta = line_lookup[line_number]

        if can_view_line(line_meta, member):
            filtered_output.append(raw_line)
        else:
            filtered_output.append(f"{line_number}: [REDACTED]")

    return filtered_output


def process_script_file(
    input_file: str,
    output_file: str,
    script_table: List[Dict[str, Any]],
    member: Dict[str, Any]
):
    """
    Reads a script file, filters it, and writes output.
    """

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    filtered_lines = filter_script(lines, script_table, member)

    with open(output_file, "w", encoding="utf-8") as f:
        for line in filtered_lines:
            f.write(line if line.endswith("\n") else line + "\n")


# -------------------------
# Example Usage
# -------------------------

script_table = [
    {
        "line_number": 1,
        "character": "Hamlet",
        "secondary_characters": ["Horatio"],
        "scene": "Act1Scene1",
        "events": [101]
    },
    {
        "line_number": 2,
        "character": "Claudius",
        "secondary_characters": [],
        "scene": "Act1Scene2",
        "events": [102]
    }
]

production_member = {
    "name": "Alice",
    "role": "Actor",
    "characters_played": ["Hamlet"],
    "characters_known": ["Horatio"],
    "scenes_known": ["Act1Scene1"],
    "major_events_known": [101]
}

# Run
process_script_file(
    "input_script.txt",
    "filtered_script.txt",
    script_table,
    production_member
)