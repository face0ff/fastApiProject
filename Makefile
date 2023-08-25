export PYTHONPATH := /home/user/PycharmProjects/fastApiProject


start_all: api parser receiver

stop_all:
	pkill -f main.py || true
	pkill -f utils.py || true
	pkill -f receiver.py || true
api:
	python src/api/main.py
parser:
	python src/parser/parser.py
receiver:
	python src/parser/receiver.py
socket:
	python src/socketio/sockets.py
client:
	python src/wallet/consumer.py

