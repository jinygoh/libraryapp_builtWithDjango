// This package contains the configuration classes for the application.
package com.example.silentlibrary.config;

// Import necessary classes.
import com.example.silentlibrary.services.MyUserDetailsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * This class configures the security settings for the application.
 * The @Configuration annotation indicates that this class contains one or more bean methods.
 * The @EnableWebSecurity annotation enables Spring Security's web security support.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfigurer {

    // The UserDetailsService is injected here to load user-specific data.
    @Autowired
    private MyUserDetailsService myUserDetailsService;

    // The JwtRequestFilter is injected here to validate the JWT.
    @Autowired
    private JwtRequestFilter jwtRequestFilter;

    /**
     * This bean configures the AuthenticationManager.
     * The AuthenticationManager is responsible for authenticating users.
     * @param http The HttpSecurity object.
     * @return The AuthenticationManager.
     * @throws Exception If an error occurs.
     */
    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http) throws Exception {
        return http.getSharedObject(AuthenticationManagerBuilder.class)
                // Use the custom UserDetailsService to load user-specific data.
                .userDetailsService(myUserDetailsService)
                // Use the password encoder to encode and decode passwords.
                .passwordEncoder(passwordEncoder())
                .and()
                .build();
    }

    /**
     * This bean configures the security filter chain.
     * The security filter chain defines which requests are secured and how they are secured.
     * @param http The HttpSecurity object.
     * @return The SecurityFilterChain.
     * @throws Exception If an error occurs.
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        // Disable CSRF (Cross-Site Request Forgery) protection.
        http.csrf().disable()
                // Authorize requests.
                .authorizeRequests()
                // Allow unauthenticated access to the /authenticate and /register endpoints.
                .requestMatchers("/authenticate", "/register").permitAll()
                // Require authentication for all other requests.
                .anyRequest().authenticated()
                .and()
                // Configure session management.
                .sessionManagement()
                // Use stateless sessions, as we are using JWTs for authentication.
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);
        // Add the JWT request filter before the username and password authentication filter.
        http.addFilterBefore(jwtRequestFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    /**
     * This bean provides a PasswordEncoder.
     * The PasswordEncoder is used to encode and decode passwords.
     * In this case, we are using NoOpPasswordEncoder, which does not perform any encoding.
     * In a real application, you should use a strong password encoder, such as BCryptPasswordEncoder.
     * @return The PasswordEncoder.
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }
}
