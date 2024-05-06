
from tools import Convert

obsiden_path = '/media/new_drive/MyNotes'
hexo_path = '/media/new_drive/eebrian123tw93.github.io/source/'


note_names = []
note_names.append('使用WebCodecs API對H264解碼')
note_names.append('H264基礎知識')
note_names.append('html隱藏元素的方法')
note_names.append('VM安裝')
note_names.append('Zigbee介紹')
note_names.append('DMA (Direct Memory Access)')
note_names.append('PWM(Pulse-width modulation)')
note_names.append('UART RS232 RS484')
note_names.append('SparkFun Thing Plus Matter - MGM240P')
note_names.append('IIC I2C （Inter-Integrated Circuit）')
note_names.append('實作 Nginx 負載平衡 load balance')
note_names.append('20240123小日常')
note_names.append('python進度條tqdm')
note_names.append('使用WebCodecs API對H265解碼')
note_names.append('Python mt5 on linux')
note_names.append('Python mt5 on macOS(M系列)')
note_names.append('share_file_descriptor(shrare fd)')
note_names.append('20240319小日常')
note_names.append('Nessus')
note_names.append('Nessus Advanced Scan')

for note_name in note_names:
    Convert(obsiden_path=obsiden_path, hexo_path=hexo_path, note_name=note_name).start()