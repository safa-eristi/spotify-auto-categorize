# -*- coding: utf-8 -*-
import os

from flaskapp import create_app


def main():
    env = os.getenv('FLASK_ENV') or 'test'
    print('Active environment: * {env} *'.format(env=env))

    app = create_app(env)
    app.run(threaded=True, debug=True, port=5003)


if __name__ == '__main__':
    main()
