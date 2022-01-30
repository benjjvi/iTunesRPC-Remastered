import module.itunesrpc_window.main as itrpc_window
from module.itrpc_logging import log_message

itrpc_window.get_logger(log_message)
itrpc_window.send_logger()

itrpc_window.start_welcome()

# itrpc_window.start(False)
