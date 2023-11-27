<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Welcome!</h1>
    <div v-if="newsStore.isAuthenticated" class="profile">
      <div class="text-center">
        <img :src="newsStore.profileImageUrl()" class="rounded-circle border border-3 border-primary" alt="Profile Image" style="width: 200px; height: 200px; object-fit: cover;">
      </div>
      <div class="mt-3 p-3 bg-light border rounded">
        <h3 class="text-primary">Profile Details</h3>
        <p class="lead"><strong>Email:</strong> {{ newsStore.userData.email }}</p>
        <p class="lead"><strong>Date of Birth:</strong> {{ newsStore.userData.date_of_birth }}</p>
        <p class="lead"><strong>Favourite Categories:</strong> {{ formattedFavoriteCategories }}</p>
      </div>
      <div class="text-center mt-3">
        <button @click="newsStore.logout()" class="btn btn-danger">Logout</button>
      </div>

      <form @submit.prevent="submitForm">
        <!-- Other input fields remain the same -->
        <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" v-model="newsStore.userData.email" required>
          </div>
          <div class="mb-3">
            <label for="dateOfBirth" class="form-label">Date of Birth</label>
            <input type="date" class="form-control" id="dateOfBirth" v-model="newsStore.userData.date_of_birth">
          </div>
          <div class="mb-3">
            <label for="profileImage" class="form-label">Profile Image</label>
            <input type="file" class="form-control" id="profileImage" @change="newsStore.onFileSelected">
          </div>
        <div class="mb-3">
          <label class="form-label">Favorite Categories</label>
          <div v-for="category in categories" :key="category.value">
            <input type="checkbox" :value="category.value" v-model="selectedCategoryIds">
            {{ category.text }}
          </div>
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
import { defineComponent, computed, onMounted, ref } from 'vue';
import { useNewsStore } from '../store/newsStore';

export default defineComponent({
  setup() {
    const newsStore = useNewsStore();
    const categories = [
      { value: '1', text: 'Sports' },
      { value: '2', text: 'World' },
      { value: '3', text: 'Finance' },
    ];

    const selectedCategoryIds = ref([]);

    const formattedFavoriteCategories = computed(() => {
      if (Array.isArray(newsStore.userData.favorite_categories)) {
        return newsStore.userData.favorite_categories.join(', ');
      }
      return '';
    });

    const submitForm = async () => {
      // Clear the old values
      newsStore.userData.favorite_categories = [];

      // Add new values (IDs)
      newsStore.userData.favorite_categories.push(...selectedCategoryIds.value);

      // Submit the updated profile
      await newsStore.updateProfile();
    };

    newsStore.fetchUserData().then(() => {
      console.log("Fetched user data:", newsStore.userData);
    }).catch(error => {
      console.error("Error fetching user data:", error);
    });

    onMounted(() => {
      newsStore.checkAuthentication();
    });

    return { 
      newsStore,
      categories,
      formattedFavoriteCategories,
      submitForm,
      selectedCategoryIds
    };
  },
});
</script>