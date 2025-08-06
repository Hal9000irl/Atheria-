# Local Development Quickstart

## Backend

```powershell
cd aetheria_backend
.\setup_backend.ps1
# Then, to run:
& .\venv\Scripts\Activate.ps1
python main.py
```

## Frontend

```powershell
cd aetheria_frontend
.\setup_frontend.ps1
# Then, to run:
flutter run
```

## Notes
- Fill in `.env` and Firebase config files as needed.
- For Android emulator, backend URL is preconfigured. For other platforms, adjust `lib/api/api_service.dart` if needed. 