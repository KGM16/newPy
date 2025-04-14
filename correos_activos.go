package main

import (
	"bufio"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

func enviarCorreo(correo string) error {
	urlStr := "https://softland.zendesk.com/access/help"
	data := url.Values{
		"authenticity_token":   {"0PpezpUpE3fWxK4hOc2dpNGgrGVknUCSalGwpRTQBE"},
		"return_to_on_failure": {"https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&return_to=https%3A%2F%2Fsoftland.zendesk.com%2Fhc%2Fes%2Frequests%3Fquery%3D%26page%3D1%26selected_tab_name%3Dmy-requests&theme=hc"},
		"return_to":            {"https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&return_to=https%3A%2F%2Fsoftland.zendesk.com%2Fhc%2Fes%2Frequests%3Fquery%3D%26page%3D1%26selected_tab_name%3Dmy-requests&theme=hc"},
		"email":                {correo},
		"brand_id":             {"360000349757"},
		"auth_origin":          {"360000349757%2Cfalse%2Ctrue"},
		"theme":                {"hc"},
		"role":                 {""},
		"commit":               {"Enviar"},
	}
	req, err := http.NewRequest("POST", urlStr, strings.NewReader(data.Encode()))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		fmt.Printf("Correo enviado a %s\n", correo)
	} else {
		fmt.Printf("Error al enviar correo a %s: %s\n", correo, resp.Status)
	}
	return nil
}

func main() {
	rutaArchivo := "C:/Users/kgomezm/newPy/correos.txt"
	rutaExisten := "C:/Users/kgomezm/newPy/logs/existen.txt"
	rutaNoExisten := "C:/Users/kgomezm/newPy/logs/no-existen.txt"

	file, err := os.Open(rutaArchivo)
	if err != nil {
		fmt.Printf("Error: El archivo %s no existe.\n", rutaArchivo)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	correosExistentes := []string{}
	correosNoExistentes := []string{}

	for scanner.Scan() {
		correo := strings.TrimSpace(scanner.Text())
		err := enviarCorreo(correo)
		if err != nil {
			fmt.Printf("Error al enviar correo a %s: %v\n", correo, err)
			correosNoExistentes = append(correosNoExistentes, correo)
		} else {
			correosExistentes = append(correosExistentes, correo)
		}
		time.Sleep(20 * time.Second) // Esperar 20 segundos antes de procesar el siguiente correo
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error al leer el archivo: %v\n", err)
	}

	// Guardar correos existentes en un archivo
	fileExisten, err := os.Create(rutaExisten)
	if err != nil {
		fmt.Printf("Error al crear el archivo %s: %v\n", rutaExisten, err)
		return
	}
	defer fileExisten.Close()
	for _, correo := range correosExistentes {
		fmt.Fprintln(fileExisten, correo)
	}

	// Guardar correos no existentes en un archivo
	fileNoExisten, err := os.Create(rutaNoExisten)
	if err != nil {
		fmt.Printf("Error al crear el archivo %s: %v\n", rutaNoExisten, err)
		return
	}
	defer fileNoExisten.Close()
	for _, correo := range correosNoExistentes {
		fmt.Fprintln(fileNoExisten, correo)
	}

	fmt.Println("Correos existentes guardados en:", rutaExisten)
	fmt.Println("Correos no existentes guardados en:", rutaNoExisten)
}
