import threading
from RecordVoice import *
from bottle import route, run

rec = RecordVoice()
@route('/record/start')
def startRec():
    if rec.isRecording == 0:
        # rec.start()
        rec.startRecording()
        return "Voice Recording Started"
    else:
        return "Voice Recording has Already Started"

@route('/record/end')
def endRec():
    if rec.isRecording == 1:
        rec.endRecording()
        return "Voice Recording Finished"
    else: 
        return "Recording is Not Started yet"

run(host='0.0.0.0', port=8080, debug=True)

