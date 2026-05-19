import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer",
                   run_on_startup=False, use_monitor=False)
def extract_titulo_receber(myTimer: func.TimerRequest) -> None:
    logging.info('tabela titulo receber.')