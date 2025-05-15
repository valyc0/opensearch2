import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class WebhookReceiver {

    public static void main(String[] args) {
        int port = 8080; // Porta su cui il server ascolterà

        try {
            // Creazione del server HTTP
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            System.out.println("Server avviato e in ascolto sulla porta " + port);

            // Configurazione dell'endpoint per il webhook
            server.createContext("/webhook", new WebhookHandler());

            // Avvio del server
            server.setExecutor(null); // Usa un executor predefinito
            server.start();
        } catch (IOException e) {
            System.err.println("Errore nell'avvio del server: " + e.getMessage());
        }
    }

    static class WebhookHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("POST".equals(exchange.getRequestMethod())) {
                // Lettura del corpo della richiesta
                byte[] requestBody = exchange.getRequestBody().readAllBytes();
                String body = new String(requestBody);

                // Log del payload ricevuto
                System.out.println("Payload ricevuto: " + body);

                // Risposta al client
                String response = "Webhook ricevuto con successo";
                exchange.sendResponseHeaders(200, response.length());
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } else {
                // Metodo non supportato
                String response = "Metodo non supportato";
                exchange.sendResponseHeaders(405, response.length());
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            }
        }
    }
}

