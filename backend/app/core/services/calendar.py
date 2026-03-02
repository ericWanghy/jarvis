import logging
import platform
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)


class CalendarService:
    def __init__(self):
        self._is_macos = platform.system() == "Darwin"
        if not self._is_macos:
            logger.info(
                "Calendar integration disabled: macOS is required for AppleScript-based calendar access"
            )

    def get_events(self, days: int = 1) -> List[Dict[str, str]]:
        """
        Get calendar events for the next N days using AppleScript.
        Returns a list of simplified event dictionaries.
        """
        if not self._is_macos:
            logger.debug("Skipping calendar fetch: not running on macOS")
            return []

        # AppleScript to get events
        # Note: This is a bit slow and fragile, but works for MVP without extra deps.
        # It fetches events from the default calendar.

        # Let's try a very simple script that returns a string summary
        script = f'''
        set startDate to current date
        set endDate to startDate + ({days} * days)

        tell application "Calendar"
            set myEvents to (every event of calendar 1 where (start date is greater than or equal to startDate) and (start date is less than or equal to endDate))
            set output to ""
            repeat with myEvent in myEvents
                set output to output & (summary of myEvent) & "|" & (start date of myEvent) & "\\n"
            end repeat
        end tell
        return output
        '''

        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                logger.error("Calendar AppleScript failed: %s", result.stderr)
                return []

            events = []
            for line in result.stdout.strip().split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    events.append({
                        "summary": parts[0].strip(),
                        "start_time": parts[1].strip()
                    })
            return events

        except subprocess.TimeoutExpired:
            logger.error("Calendar AppleScript timed out after 10 seconds")
            return []
        except FileNotFoundError:
            logger.error("osascript not found; calendar integration requires macOS")
            return []
        except Exception as e:
            logger.error("Failed to fetch calendar: %s", e)
            return []
