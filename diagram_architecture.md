flowchart TD
    subgraph User["User (Recruiter)"]
        Browser["Web Browser (HTML/CSS/JS)"]
    end

    subgraph Frontend["Frontend"]
        A1["Home (Avatar + XP + Level)"]
        A2["Quests Page (Projects)"]
        A3["Skills Page (Badges)"]
    end

    subgraph Backend["Backend - Flask (Python)"]
        API1["/api/player"]
        API2["/api/quests"]
        API3["/api/skills"]
    end

    subgraph Data["Data (JSON)"]
        P["player.json"]
        Q["quests.json"]
        S["skills.json"]
    end

    subgraph External["External Services"]
        GH["GitHub (project repos)"]
        Host["Netlify / Render / Heroku"]
    end

    User --> Browser
    Browser --> Frontend
    Frontend --> Backend
    Backend --> Data
    Frontend -->|Links| GH
    Backend --> Host
