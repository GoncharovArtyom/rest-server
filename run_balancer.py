from balancer import app
from balancer.config import BALANCER_PORT

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=BALANCER_PORT)
