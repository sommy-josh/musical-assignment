from locust import HttpUser, task, between

class MusicAPIUser(HttpUser):
    wait_time = between(1, 3)  # Simulate users waiting between 1-3 seconds between requests

    @task(2)  # Run this task more frequently (2x weight)
    def get_artists(self):
        """Simulates users fetching a list of artists."""
        self.client.get("/artists/")

    @task(1)  # Normal weight
    def get_albums(self):
        """Simulates users fetching a list of albums."""
        self.client.get("/albums/")

    @task(1)
    def get_tracks(self):
        """Simulates users fetching a list of tracks."""
        self.client.get("/tracks/")

    @task(3)  # Simulates login requests (3x weight)
    def login(self):
        """Simulates users logging in."""
        self.client.post("/auth/login/", json={"login_id": "testuser@example.com", "password": "testpass123"})
