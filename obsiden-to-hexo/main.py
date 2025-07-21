
from concurrent.futures import ProcessPoolExecutor


def convert_note_task(note_name, obsiden_path, hexo_path):
    from tools import Convert
    Convert(obsiden_path=obsiden_path, hexo_path=hexo_path, note_name=note_name).start()

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
note_names.append('LDAP')

note_names.append('20240701小日常 1')
note_names.append('20240701小日常 2')
note_names.append('20240701小日常 3')

note_names.append('sonarqube')


note_names.append('WebRTC基礎')
note_names.append('NAT（Network Address Translation，網路位址轉換）')
note_names.append('P2P 打洞（Peer-to-Peer NAT Traversal）')
note_names.append('STUN（ Session Traversal Utilities for NAT，NAT 穿越會話工具）')
note_names.append('TURN 協議（Traversal Using Relays around NAT）')
note_names.append('信令服務器')
note_names.append('ICE Interactive Connectivity Establishment，交互式连接建立')
note_names.append('RTCP（Real-time Transport Control Protocol）')
note_names.append('RTP（Real-time Transport Protocol）')
note_names.append('SDP（Session Description Protocol, 会话描述协议）')
note_names.append('WebRTC 使用了哪些協定')
note_names.append('ICE連線排序規則')
note_names.append('PeerConnection 連線過程')
note_names.append('搭建webrtc服务器')
note_names.append('編譯程式碼webrtc')
note_names.append('Webrtc視訊流')



note_names.append('20250214小日常-WebSocket IDR Frame delay')
note_names.append('Nessus scan issue- ICMP Timestamp Request Remote Date Disclosure')
note_names.append('lru_cache 不要亂用')

note_names.append('git flow')
note_names.append('git常用指令')


with ProcessPoolExecutor() as executor:
    futures = [
        executor.submit(convert_note_task, note_name, obsiden_path, hexo_path)
        for note_name in note_names
    ]

    # 等待所有任务完成并处理可能的异常
    for future in futures:
        future.result()