# Acesso Remoto do NVDA
Versão 2.2

Bem-vindo ao extra do Acesso Remoto do NVDA, que lhe permitirá ligar-se a outro computador que esteja a executar o  NVDA. Não faz diferença se  estiver do outro lado da sala ou do outro lado do mundo. A ligação é simples e há poucos comandos para memorizar. Pode ligar-se ao computador de outra pessoa ou permitir que uma pessoa confiável se ligue ao seu sistema para realizar uma manutenção de rotina, diagnosticar um problema ou fornecer-lhe instruções de treino.

## Antes de  começar

Precisará de instalar o NVDA em ambos os computadores e obter o extra  de Acesso Remoto do NVDA.
A instalação do NVDA e do addon Remote Access é padrão. Se precisar de mais informações,  pode  encontrá-las no Guia do Usuário do NVDA.

## Actualizar

Ao actualizar o extra, se  instalou o NVDA Remote na área de trabalho protegida, é recomendável também actualizar a cópia na área de trabalho protegida.
Para fazer isso, primeiro actualize o seu extra. Em seguida, abra o menu do NVDA, as preferências, as configurações,  gerais e pressione o botão "Utilizar as configurações actualmente guardadas no ecrã de início de sessão e noutros ecrãs (requer privilégios de administrador)".

## Iniciar uma sessão remota através de um servidor de retransmissão
### No computador a ser controlado
1. Abra o menu do NVDA, Ferramentas, Remoto, ligar.
2. Escolha cliente no primeiro botão de opção.
3. Seleccione "Permitir que este  computador seja controlado", no segundo conjunto de botões de opção.
4. No campo host, insira o host do servidor ao qual  se está a ligar, por exemplo nvdaremote.com. Quando o servidor em particular usa uma porta alternativa,  pode inserir o host no formulário u0026 lt; host u0026 gt ;: u0026 lt; porta u0026 gt ;, por exemplo nvdaremote.com:1234.
5. Digite um código no campo-código ou pressione o botão gerar código.
O código é o que os outros usarão para controlar o seu computador.
A máquina que está a ser controlada e todos os seus clientes precisam de usar o mesmo código.
6. Pressione ok. Uma vez feito,  ouvirá um beep e a palavra "ligado".

### Na máquina que será o computador de controlo
1. Abra o menu do NVDA, Ferramentas, Remoto, ligar.
2. Escolha cliente no primeiro botão de opção.
3. Seleccione Controlar outro computador, no segundo conjunto de botões de opção.
4. No campo host, insira o host do servidor ao qual  se está a ligar, por exemplo nvdaremote.com. Quando o servidor em particular usa uma porta alternativa,  pode inserir o host no formulário u0026 lt; host u0026 gt ;: u0026 lt; porta u0026 gt ;, por exemplo nvdaremote.com:1234.
5. Digite um código, no campo-código ou pressione o botão gerar código.
A máquina que está a ser controlada e todos os seus clientes precisam de usar o mesmo código.
6. Pressione ok. Uma vez feito,  ouvirá um beep e a palavra "ligado".

## ligações directas
A opção do servidor na caixa de diálogo de ligação permite que  configure uma ligação directa.
Uma vez seleccionado, escolha  o modo em que o final da conexão estará.
A outra pessoa  ligar-se-á  a você usando o oposto.

Quando o modo estiver seleccionado,  pode usar o botão Obter o IP externo para obter o endereço IP externo e
Certifique-se de que a porta inserida no campo da porta seja encaminhada corretamente.
Se o portcheck detectar que sua porta (6837 por padrão) não está acessível, um aviso será mostrado.
Encaminhe a sua porta e tente novamente.
Nota: O processo para encaminhar portas está fora do escopo deste documento. Por favor, consulte as informações fornecidas com o seu roteador para mais instruções.

Digite um código no campo-código ou pressione gerar. A outra pessoa precisará do seu IP externo junto com o código para se conectar. Se você inseriu uma porta diferente do padrão (6837) no campo da porta, verifique se a outra pessoa anexou a porta alternativa ao endereço do host no formato u0026 lt; external ip u0026 gt;: u0026 lt; port u0026 gt ;.

Uma vez que "ok" seja  pressionado,  será ligado.
Quando a outra pessoa se liga,  pode usar o acesso remoto do NVDA normalmente.

## Controlar a máquina remota

Uma vez que a sessão é iniciada, o utilizador da máquina controladora pode pressionar f11 para começar a controlar a máquina remota (por exemplo, enviando as teclas do teclado ou entrada em braille).
Quando o NVDA diz que controla a máquina remota, as teclas do teclado e da linha braille pressionadas irão para a máquina remota. Além disso, quando a máquina controladora estiver a usar uma linha braille, as informações da máquina remota serão exibidas nela. Pressione f11 novamente para parar de enviar as teclas e voltar para a máquina controladora.
Para melhor compatibilidade, certifique-se de que os layouts de teclado nas duas máquinas correspondam.

## Compartilhar a sua sessão

Para compartilhar uma ligação, para que outra pessoa possa participar facilmente da sua sessão do acesso remoto do NVDA, seleccione Copiar ligação, no menu Remoto.
Se  estiver conectado como o computador controlador, esse link permitirá que outra pessoa se conecte e seja controlada.
Se, em vez disso,  configurar o seu computador para ser controlado, a ligação permitirá que as pessoas com quem você o compartilhe controlem sua máquina.
Muitos aplicativos permitem que os utilizadores activem essa ligação automaticamente, mas se ele não for executado num aplicativo específico, ele poderá ser copiado para a área de transferência e executado a partir da caixa de diálogo de execução.


## Enviar Ctrl + Alt + Del
Durante o envio de teclas, não é possível enviar a combinação CTRL + Alt + del normalmente.
Se  precisar de enviar CTRL + Alt + del, e o sistema remoto estiver na área de trabalho protegida, use este comando.

## Controlar remotamente um computador autônomo

Às vezes,  pode querer controlar um dos seus computadores remotamente. Isso é especialmente útil se  estiver a viajar e desejar controlar o seu PC doméstico a partir do seu laptop. Ou, pode querer controlar um computador numa sala da sua casa enquanto está sentado do lado de fora com outro PC. Uma preparação pouco avançada torna isso conveniente e possível.

1. Entre no menu do NVDA e seleccione Ferramentas, depois Remoto. Finalmente, pressione Enter nas Opções.
2. Marque a caixa que diz "ligar automaticamente ao servidor de controlo ao iniciar".
3. Seleccione se deseja usar um servidor de retransmissão remota ou hospedar localmente a ligação.
4. Seleccione Permitir que esta máquina seja controlada no segundo conjunto de botões de opção.
5. Se  você mesmo hospedar a conexão, precisará garantir que a porta inserida no campo da porta (6837 por padrão) na máquina controlada possa ser acedida a partir das máquinas controladoras.
6. Se  deseja usar um servidor de retransmissão, preencha os campos Host e código, clique em OK e pressione Enter. A opção Gerar código não está disponível nesta situação. É melhor criar um código de que se lembre, para poder usá-lo facilmente em qualquer local remoto.

Para uso avançado,  também pode configurar o acesso remoto do NVDA  para se ligar automaticamente a um servidor de retransmissão local ou remoto no modo de controlo. Se  quiser isso, seleccione Controlar outra máquina no segundo conjunto de botões de opção.

Nota: A ligação automática nas opções relacionadas à inicialização na caixa de diálogo de opções não se aplica até que o NVDA seja reiniciado.


## Silenciar a voz no computador remoto
Se  não deseja ouvir a fala do computador remoto ou os sons específicos do NVDA, simplesmente aceda ao menu do NVDA, Ferramentas e Remoto. Seta para baixo para silenciar remoto e pressione Enter. Por favor, note que esta opção não irá desabilitar a saída em braille remoto para a linha braille de controlo quando a máquina controladora estiver a enviar os códigos.


## Fechar uma sessão remota

Para finalizar uma sessão remota, faça o seguinte:

1. No computador de controlo, pressione F11 para parar de controlar a máquina remota. Deve ouvir ou ler a mensagem: "Controlando a máquina local". Se, em vez disso, você ouvir ou ler uma mensagem informando que está a controlar a máquina remota, pressione F11 mais uma vez.

2. Aceda ao menu do NVDA, depois Ferramentas, Remoto, e pressione Enter em desligar.

## Empurrar a área de transferência
A opção empurrar a área de transferência no menu remoto permite que  envie texto da sua área de transferência.
quando activado, qualquer texto na área de transferência será empurrado para as outras máquinas.

## Configurar o acesso remoto do NVDA para funcionar em um desktop seguro

Para que o acesso remoto do NVDA  funcione na área de trabalho protegida, o extra deve ser instalado no NVDA em execução na área de trabalho protegida.

1. No menu do NVDA, Escolha Preferências e, em seguida, Configurações, gerais.

2. Aceda ao separador "Utilizar as configurações actualmente guardadas no ecrã de início de sessão e noutros ecrãs seguros (requer privilégios de administrador) e pressione Enter.

3. Responda Sim aos prompts relacionados com a  cópia das suas configurações e sobre como copiar plug-ins e responda ao prompt do Controlo de Conta de Usuário que pode aparecer.
4. Quando as configurações forem copiadas, pressione Enter para descartar o botão OK. Tab para OK e Enter mais uma vez para sair da caixa de diálogo.

Depois que o acesso remoto do NVDA  for instalado na área de trabalho segura, se  estiver sendo controlado em uma sessão remota,
 terá acesso de voz e braille à área de trabalho protegida quando alternado.

## Contribuições
Gostaríamos de agradecer aos seguintes colaboradores, entre outros, que ajudaram a tornar o projeto do acesso remoto do NVDA  uma realidade.

* Hai Nguyen Ly
* Chris Westbrook
* Thomas Huebner
* John F Crosotn III
* Darrell Shandrow
* D Williams
* Matthew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews
* Babbage B.V.
* Leonard de Ruijter

## Mudanças

### Versão 2.2

* Suporte IPv6
* Suporte para o novo NVDA 2018.3, bem como versões mais antigas
* Suporte para  comandos Braille específicos do modelo


### Versão 2.1

* Conexão fixa não salva ao permitir que esta máquina seja controlada
* Adicionado um script para empurrar a área de transferência com ctrl + shift + NVDA + c
* A Entrada em braille agora funciona no modo de navegação
* Comandos  braille específicos do modelo de suporte
* Os bips gerados pelo NVDA Remote não bloqueiam mais o NVDA

### Versão 2.0

* Suporte remoto para Braille
* Suporte para acesso remoto do nvda: // ligações
* Diálogos centralizados para se adequar ao resto do NVDA
* Corrigido portcheck para apontar em um domínio que controlamos, portcheck.nvdaremote.com
* Suporte conectando-se automaticamente a um servidor de controle no modo mestre
* Corrigido erro de renderização na documentação
* Actualização para a versão 2 do protocolo, que inclui um campo de origem em todas as mensagens remotas
* Limpeza de código  permitindo modificações mais fáceis, no futuro