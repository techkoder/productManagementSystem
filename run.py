from app import models
import os
app = models.create_app(os.environ.get('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
