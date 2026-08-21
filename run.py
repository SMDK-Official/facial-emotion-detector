import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # In Codespaces, bind to 0.0.0.0 so the port forwarder can route traffic
    app.run(host='0.0.0.0', port=port, debug=True)