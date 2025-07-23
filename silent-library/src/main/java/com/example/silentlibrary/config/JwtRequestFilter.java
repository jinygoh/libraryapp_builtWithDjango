// This package contains the configuration classes for the application.
package com.example.silentlibrary.config;

// Import necessary classes.
import com.example.silentlibrary.services.MyUserDetailsService;
import com.example.silentlibrary.utils.JwtUtil;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

/**
 * This class is a filter that intercepts incoming requests to validate the JWT.
 * It extends OncePerRequestFilter to ensure that it is executed only once per request.
 */
@Component
public class JwtRequestFilter extends OncePerRequestFilter {

    // The UserDetailsService is injected here to load user-specific data.
    @Autowired
    private MyUserDetailsService userDetailsService;

    // The JwtUtil is injected here to work with JWTs.
    @Autowired
    private JwtUtil jwtUtil;

    /**
     * This method is called for each incoming request.
     * It extracts the JWT from the request header, validates it, and sets the authentication in the security context.
     * @param request The incoming request.
     * @param response The outgoing response.
     * @param chain The filter chain.
     * @throws ServletException If a servlet-specific error occurs.
     * @throws IOException If an I/O error occurs.
     */
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {

        // Get the Authorization header from the request.
        final String authorizationHeader = request.getHeader("Authorization");

        String username = null;
        String jwt = null;

        // Check if the Authorization header is present and starts with "Bearer ".
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            // Extract the JWT from the header.
            jwt = authorizationHeader.substring(7);
            // Extract the username from the JWT.
            username = jwtUtil.extractUsername(jwt);
        }

        // If the username is not null and there is no authentication in the security context.
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            // Load the user details from the database.
            UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);
            // Validate the JWT.
            if (jwtUtil.validateToken(jwt, userDetails)) {
                // If the JWT is valid, create a new authentication token.
                UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken = new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());
                // Set the details of the authentication token.
                usernamePasswordAuthenticationToken
                        .setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                // Set the authentication in the security context.
                SecurityContextHolder.getContext().setAuthentication(usernamePasswordAuthenticationToken);
            }
        }
        // Continue the filter chain.
        chain.doFilter(request, response);
    }
}
