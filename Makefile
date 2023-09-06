export PYTHONPATH := /home/user/PycharmProjects/fastApiProject


start_all: api parser receiver

stop_all:
	pkill -f main.py || true
	pkill -f utils.py || true
	pkill -f receiver.py || true
api:
	python src/api/main.py
parser:
	python src/parser/parser_socket.py
receiver:
	python src/parser/receiver.py
socket:
	python src/socketio/sockets.py
client:
	python src/wallet/consumer.py
ibay:
	python src/ibay/consumer.py
celery:
	celery -A src.celery.celery worker --loglevel=info -Q periodic,permission,wallet,save_result,transaction,search_transaction,check_delivery -B --concurrency=4


