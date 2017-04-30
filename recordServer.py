import threading
from RecordVoice import *
from bottle import route, run

rec = RecordVoice()
@route('/record/start')
def startRec():
    if reg.isRecording == 0:
        # reg.start()
        reg.startRecording()
        return "Voice Recording Started"
    else:
        return "Voice Recording has Already Started"

@route('/record/end')
def endRec():
    if reg.isRecording == 1:
        reg.endRecording()
        return "Voice Recording Finished"
    else: 
        return "Recording is Not Started yet"

threading.Thread(target=run, kwargs=dict(host='localhost', port=8080, debug=True)).start()


