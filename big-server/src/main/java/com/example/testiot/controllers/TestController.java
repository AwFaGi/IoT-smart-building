package com.example.testiot.controllers;

import org.apache.coyote.Response;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController("**")
public class TestController {

    @GetMapping("/**")
    public ResponseEntity<?> test() {
        return ResponseEntity.ok("ok");
    }

    @PostMapping("/**")
    public ResponseEntity<?> test2() {
        return ResponseEntity.ok("ok");
    }
}
