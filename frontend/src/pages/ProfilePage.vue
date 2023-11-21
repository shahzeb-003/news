<template>
    <div class="container my-5">
      <h1 class="text-center mb-4">Welcome!</h1>
      <div v-if="isAuthenticated" class="profile">
  
        <div class="text-center">
          <img :src="profileImageUrl" class="rounded-circle border border-3 border-primary" alt="Profile Image" style="width: 200px; height: 200px; object-fit: cover;">
        </div>
        <div class="mt-3 p-3 bg-light border rounded">
          <h3 class="text-primary">Profile Details</h3>
          <p class="lead"><strong>Email:</strong> {{ userData.email }}</p>
          <p class="lead"><strong>Date of Birth:</strong> {{ userData.date_of_birth }}</p>
          <p class="lead"><strong>Favourite Category:</strong> {{ userData.favorite_category }}</p>
        </div>
        <div class="text-center mt-3">
          <button @click="logout" class="btn btn-danger">Logout</button>
        </div>
  
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" v-model="userData.email" required>
          </div>
          <div class="mb-3">
            <label for="dateOfBirth" class="form-label">Date of Birth</label>
            <input type="date" class="form-control" id="dateOfBirth" v-model="userData.date_of_birth">
          </div>
          <div class="mb-3">
            <label for="profileImage" class="form-label">Profile Image</label>
            <input type="file" class="form-control" id="profileImage" @change="onFileSelected">
          </div>
          <div class="mb-3">
          <label for="favoriteCategory" class="form-label">Favorite Category</label>
          <select id="favoriteCategory" class="form-control" v-model="userData.favorite_category" required>
            <option value="">Select a category</option>
            <option value="SP">Sports</option>
            <option value="WR">World</option>
            <option value="FN">Finance</option>
          </select>
        </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
      </div>
      <div v-else class="alert alert-warning" role="alert">
        <p>Please log in to access this content.</p>
      </div>
    </div>
</template>
  
    
<script lang="ts">
      import { defineComponent } from "vue";
      // In your Vue component
    
    export default defineComponent({
      data() {
        return {
          userData: {
            email: '',
            date_of_birth: '',
            profile_image: '',
            favorite_category: ''
          },
          isAuthenticated: false,
          selectedFile: null as File | null,
        };
      },
      computed: {
        profileImageUrl() {
          return `http:///127.0.0.1:8000${this.userData.profile_image}`;
        }
      },
      methods: {
        async logout() {
          try {
            const response = await fetch('http://127.0.0.1:8000/api/logout/', {
              method: 'POST',
              credentials: 'include', // Use 'include' to send cookies
            });
    
            if (response.ok) {
              window.location.href = 'http://127.0.0.1:8000/login/';
            } else {
              // Handle logout failure
              console.error('Logout failed:', response.status, response.statusText);
            }
          } catch (error) {
            console.error('Logout failed:', error);
            // Handle logout failure
          }
        },
        async fetchUserData() {
          try {
            fetch(`http://127.0.0.1:8000/api/user-details/`, {
              method: "GET",
              credentials: 'include',
              headers: {
                "Content-Type": "application/json",
              },
            })
            .then((response) => response.json())
            .then((data) => {
              if (data.error) {
              // User is not authenticated
              this.isAuthenticated = false;
            } else {
              // User is authenticated
              console.log(data);
              this.userData = data;
              this.isAuthenticated = true;
            }
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
            });
          } catch (error) {
            console.error('Error fetching user data:', error);
            // Handle error (e.g., redirect to login if unauthorized)
          }
        },
        onFileSelected(event: Event) {
          const input = event.target as HTMLInputElement;
          if (input.files) {
            this.selectedFile = input.files[0];
            // Create a local URL for the file to display it immediately
            this.userData.profile_image = URL.createObjectURL(this.selectedFile);
          }
        },
  
        async updateProfile() {
          const formData = new FormData();
          formData.append('email', this.userData.email);
          formData.append('date_of_birth', this.userData.date_of_birth);
          formData.append('favorite_category', this.userData.favorite_category)
          if (this.selectedFile) {
            formData.append('profile_image', this.selectedFile, this.selectedFile.name);
          }
  
          try {
            const response = await fetch('http://127.0.0.1:8000/api/update-user-details/', {
              method: 'POST',
              credentials: 'include',
              body: formData,
            });
  
            if (response.ok) {
              console.log('Profile updated successfully');
              // Re-fetch user data to get updated information
              this.fetchUserData();
            } else {
              console.error('Profile update failed:', response.status, response.statusText);
            }
          } catch (error) {
            console.error('Profile update failed:', error);
          }
        },
    },
  
      created() {
          this.fetchUserData();
      }
    });
</script>
