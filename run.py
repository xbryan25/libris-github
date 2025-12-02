import eventlet
import os

eventlet.monkey_patch()  # noqa: E402

from app import create_app, socketio  # noqa: E402

app = create_app()
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
    from app.scheduler import init_scheduler

    init_scheduler(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
