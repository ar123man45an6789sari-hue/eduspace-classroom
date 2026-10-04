# AI Assistant

The `ai_assistant` app provides permission-scoped AI tools for the existing classroom system:

- Students can ask questions grounded in materials from enrolled classrooms.
- Teachers can draft assignments, summarize materials, generate quizzes, and request submission review suggestions.
- AI review suggestions are sent to the existing grade form and are never saved automatically.

## Configuration

Set `GEMINI_API_KEY` in the server environment or in the local ignored `.env` file. `GEMINI_MODEL` is optional and defaults to `gemini-3.6-flash`. The key is read server-side by `AIProvider` and is never rendered into templates or sent to the browser.

Document extraction supports `.pdf`, `.docx`, `.txt`, and `.md`. Unsupported or unreadable files produce a user-facing error message.
