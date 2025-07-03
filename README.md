# NerdSystem Bot
Este bot é um bot para fazer uma integração do Simply Plural usando a API e o WebSocket provinciado por eles, para assim melhorar a experiência para sistemas TDI no Discord. 
Receber eventos (no caso de WebSocket) de quando uma alter muda de controle, e modificar algumas coisas (com a API), como o frontHistory, que dá pra fazer uma alter começar a front ou terminar de frontar.
Com esse bot, é possível receber eventos pelo WebSocket, quando uma alter muda, e esse evento dispara um outro evento, que é o evento do bot, que manda uma mensagem
para o nosso servidor pessoal onde pessoas podem saber quando uma entrou ou saiu do front.
Também há comandos para sair e entrar do front, sendo dois deles são front e unfront, que vão verificar quem fez o comando e se for alguma de nós, ele vai colocar no front
a alter que fez o comando, e os outros dois, o setalterfront e removealterfront, que serve para quando queremos manipular o front de outra que não seja ela mesma, para
caso uma esqueça de sair do front, uma avisar e outra fazer o comando para deixar de forma organizada.
