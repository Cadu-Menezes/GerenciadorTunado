import psutil 
import pygame
import cpuinfo


def mostra_info_cpu():
  s1.fill(branco)
  mostra_texto(s1, "Nome:", "brand_raw", 10)
  mostra_texto(s1, "Arquitetura:", "arch", 30)
  mostra_texto(s1, "Palavra (bits):", "bits", 50)
  mostra_texto(s1, "Frequência (MHz):", "freq", 70)
  mostra_texto(s1, "Núcleos (físicos):", "nucleos", 90)
  tela.blit(s1, (0, 0))


def mostra_texto(s1, nome, chave, pos_y):
  text = font.render(nome, True, preto)
  s1.blit(text, (10, pos_y))
  if chave == "freq":
          s = str(round(psutil.cpu_freq().current, 2))
  elif chave == "nucleos":
          s = str(psutil.cpu_count())
          s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
  else:
          s = str(info_cpu[chave])
  text = font.render(s, True, cinza)
  s1.blit(text, (230, pos_y))


def mostra_uso_cpu(s, l_cpu_percent):
  s.fill(preto)
  num_cpu = len(l_cpu_percent)
  x = y = 10
  desl = 10
  alt = s.get_height() - 2*y
  larg = (s.get_width()-2*y - (num_cpu+1)*desl)/num_cpu
  d = x + desl
  for i in l_cpu_percent:
              pygame.draw.rect(s, vermelho, (d, y, larg, alt))
              pygame.draw.rect(s, azul,     (d, y, larg, (1-i/100)*alt))
              d = d + larg + desl
  # parte mais abaixo da tela e à esquerda
  tela.blit(s, (0, altura_tela/5))


def mostra_uso_disco():
    disco = psutil.disk_usage('.')
    larg = largura_tela -2*20
    pygame.draw.rect(s3, azul, (20, 50, largura_tela-2*20, 70)) 
    larg = larg*disco.percent/100
    pygame.draw.rect(s3, vermelho, (20, 50, larg, 70))
    tela.blit(s3, (0, 2*altura_tela/4))
    total =  round(disco.total/(1024**3), 2)
    texto_barra = "Uso de Disco: (Total: " +str(total) + " GB):"
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 420))  


def mostra_uso_memoria():    
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20 
    tela.fill(preto)
    pygame.draw.rect(s4, azul, (20, 50, largura_tela-2*20, 70))
    larg = larg*mem.percent/100     
    pygame.draw.rect(s4, vermelho, (20, 50, larg, 70))
    tela.blit(s4, (0, 3*altura_tela/4))
    total = round(mem.total/(1024**3), 1) 
    texto_barra = "Uso de memória (Total: " + str(total) + "GB): " 
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 600)) 


def endereço ():
    dic_interfaces = psutil.net_if_addrs()
    ip = dic_interfaces["Ethernet"][1].address
    larg = largura_tela -2*20
    texto_ip = f"Endereço IP: {ip}" 
    text = font.render(texto_ip, 1, branco)
    tela.blit(text, (20, 750))


info_cpu = cpuinfo.get_cpu_info()


azul = (0, 0, 255)  
vermelho = (255, 0, 0)  
branco = (255, 255, 255) 
preto = (0, 0, 0)
cinza = (100, 100, 100)


pygame.font.init()
font = pygame.font.Font(None, 32)


largura_tela = 1000   
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Gerenciador de Tarefas ")   # Título da tela de tarefas. 
pygame.display.init()


s1 = pygame.surface.Surface((largura_tela, altura_tela/4))
s2 = pygame.surface.Surface((largura_tela, altura_tela/4))
s3 = pygame.surface.Surface((largura_tela, altura_tela/4))
s4 = pygame.surface.Surface((largura_tela, altura_tela/4))


pygame.draw.rect(s1, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s1, (0, 0))

pygame.draw.rect(s2, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s2, (0, altura_tela/4))

pygame.draw.rect(s3, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s3, (0, 2*altura_tela/4))

pygame.draw.rect(s4, azul, (20, 50, largura_tela-2*20, 70))
tela.blit(s4, (0, 2*altura_tela/4))


clock = pygame.time.Clock()   # Criar relógio.


cont = 30 
terminou = False 
while not terminou:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            terminou = True    

    if cont == 30: 
        mostra_uso_memoria()
        mostra_uso_cpu(s1, psutil.cpu_percent(interval=1, percpu=True))   
        mostra_uso_disco()  
        endereço () 
        mostra_info_cpu()
        cont = 0   
   
    pygame.display.update()  
    clock.tick(60) 
    cont = cont + 1  

pygame.display.quit()