// This is the main package for the Silent Library application.
package com.example.silentlibrary;

// Import necessary classes from the Spring Framework.
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * This is the main class for the Silent Library application.
 * The @SpringBootApplication annotation enables auto-configuration, component scanning,
 * and other features that make it easy to develop Spring Boot applications.
 */
@SpringBootApplication
public class SilentLibraryApplication {

	/**
	 * The main method, which serves as the entry point for the application.
	 * It uses SpringApplication.run() to launch the Spring Boot application.
	 * @param args Command-line arguments.
	 */
	public static void main(String[] args) {
		// Launch the Spring Boot application.
		SpringApplication.run(SilentLibraryApplication.class, args);
	}

}
