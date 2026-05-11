from api.base_api import BaseAPI

from config.environment import config

from utils.logger import get_logger


logger = get_logger(__name__)


class NotesAPI(BaseAPI):

    def __init__(self, token):

        headers = {
            "x-auth-token": token
        }

        super().__init__(
            config.api_url,
            headers=headers
        )

    def get_notes(self):

        logger.info(
            "Fetching notes via API"
        )

        return self.get("/notes")

    def create_note(
        self,
        title,
        description,
        category="Home",
        completed=False
    ):

        logger.info(
            f"Creating note via API: "
            f"{title}"
        )

        payload = {
            "title": title,
            "description": description,
            "category": category,
            "completed": completed
        }

        return self.post(
            "/notes",
            payload
        )

    def update_note(
        self,
        note_id,
        title,
        description,
        category="Work",
        completed=True
    ):

        logger.info(
            f"Updating note via API: "
            f"{note_id}"
        )

        payload = {
            "title": title,
            "description": description,
            "category": category,
            "completed": completed
        }

        return self.put(
            f"/notes/{note_id}",
            payload
        )

    def delete_note(self, note_id):

        logger.info(
            f"Deleting note via API: "
            f"{note_id}"
        )

        return self.delete(
            f"/notes/{note_id}"
        )

    def delete_all_notes(self):

        logger.info(
            "Deleting all notes"
        )

        response = self.get_notes()

        notes = response.json().get(
            "data",
            []
        )

        for note in notes:

            note_id = note["id"]

            delete_response = (
                self.delete_note(note_id)
            )

            logger.info(
                f"Deleted note: {note_id} "
                f"| Status: "
                f"{delete_response.status_code}"
            )