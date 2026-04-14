import os

############################################
# LÓGICA VELOCIDADE
############################################

traffic_record_folder_name = "TrafficRecord"

if not os.path.exists(traffic_record_folder_name):
    os.makedirs(traffic_record_folder_name)
    os.makedirs(traffic_record_folder_name+"//exceeded")


speed_record_file_location = traffic_record_folder_name + "//SpeedRecord.txt"
file = open(speed_record_file_location, "w")
file.write("ID \t SPEED\n------\t-------\n")
file.close()

def registrar_entrada(track_id, timeA, track_states):
    # Se time_A ainda é None, definimos
    if track_states[track_id]["time_A"] is None:
        track_states[track_id]["time_A"] = timeA

def registrar_saida(track_id, timeB, track_states, DISTANCIA_LINHAS_METROS):
    if not track_states[track_id]["has_crossed_B"]:
        track_states[track_id]["has_crossed_B"] = True
        track_states[track_id]["time_B"] = timeB

        tA = track_states[track_id]["time_A"]
        tB = track_states[track_id]["time_B"]
        if tA is not None:
            dt = tB - tA
            if dt > 0:
                ms = DISTANCIA_LINHAS_METROS / dt
                kmh = ms * 3.6
                track_states[track_id]["speed"] = kmh
                print(f"[INFO] track {track_id} => velocidade = {kmh:.2f} km/h")
                
                n = str(track_id) + "_speed_" + str(kmh)
                file = traffic_record_folder_name + '//' + n + '.jpg'
                filet = open(speed_record_file_location, "a")
                file2 = traffic_record_folder_name + '//exceeded//' + n + '.jpg'
                filet.write(str(track_id) + " \t " + str(kmh) + "<---exceeded\n")

    track_states[track_id]["active"] = False
    
    # return kmh