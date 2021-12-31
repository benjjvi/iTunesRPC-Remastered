from module.itrpc_logging import log_message
import module.itunesrpc_window.main as itrpc_window

itrpc_window.get_logger(log_message)
itrpc_window.send_logger()