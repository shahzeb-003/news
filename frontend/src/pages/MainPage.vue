<template>
  <div class="container mt-4">
    <div v-if="newsStore.isAuthenticated" class="profile">
      <h3 class="mb-3">{{ title }}</h3>
      <div v-for="newsItem in newsStore.newsList" :key="newsItem.id" class="mb-5">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">{{ newsItem.title}}</h4>
            <p class="card-text">{{ newsItem.text }}</p>
          </div>
        </div>

        <!-- Comments Section -->
        <div class="mt-4">
          <h5>Comments</h5>
          <div v-for="comment in newsItem.comments" :key="comment.id" class="card mb-2">
            <div class="card-body">
              <!-- Display Comment or Edit Form -->
              <div v-if="newsStore.editingCommentId !== comment.id">
                <p><strong>{{ comment.author_email }}:</strong> {{ comment.text }}</p>
                <button v-if="comment.author_email === newsStore.userData.email" class="btn btn-sm btn-outline-secondary" @click="newsStore.startEditing(comment)">Edit</button>
                <button v-if="comment.author_email === newsStore.userData.email" class="btn btn-sm btn-outline-danger" @click="newsStore.deleteComment(comment.id)">Delete</button>
                <button class="btn btn-sm btn-outline-primary" @click="newsStore.startReply(comment.id, comment.author_email)">Reply</button>
              </div>
              <div v-else>
                <input class="form-control" type="text" v-model="newsStore.editedCommentText">
                <button class="btn btn-sm btn-success" @click="newsStore.submitEdit(comment.id)">Save</button>
                <button class="btn btn-sm btn-warning" @click="newsStore.cancelEditing">Cancel</button>
              </div>

              <!-- ... Replies and Reply Form ... -->

              <div v-for="reply in comment.replies" :key="reply.id" class="ml-4 mt-2 card bg-light">
                <div class="card-body">
                  <div v-if="newsStore.editingCommentId !== reply.id">
                    <p><strong>{{ reply.author_email }}</strong> replying to <strong>{{ comment.author_email }}:</strong> {{ reply.text }}</p>
                    <button v-if="reply.author_email === newsStore.userData.email" class="btn btn-sm btn-outline-secondary" @click="newsStore.startEditing(reply)">Edit</button>
                    <button v-if="reply.author_email === newsStore.userData.email" class="btn btn-sm btn-outline-danger" @click="newsStore.deleteComment(reply.id)">Delete</button>
                  </div>
                  <div v-else>
                    <input class="form-control" type="text" v-model="newsStore.editedCommentText">
                    <button class="btn btn-sm btn-success" @click="newsStore.submitEdit(reply.id)">Save</button>
                    <button class="btn btn-sm btn-warning" @click="newsStore.cancelEditing()">Cancel</button>
                  </div>
                </div>
              </div>
              <!-- Reply Form -->
              <div v-if="newsStore.replyingTo === comment.id" class="mt-2">
                  <input class="form-control mb-2" type="text" v-model="newsStore.commentText" placeholder="Replying to {{ newsStore.replyingToEmail }}">
                  <button class="btn btn-sm btn-success" @click="newsStore.submitReply(newsItem.id)">Submit Reply</button>
                  <button class="btn btn-sm btn-warning" @click="newsStore.cancelEditing()">Cancel</button>
                </div>
            </div>
          </div>

          <!-- Form to submit a new top-level comment -->
          <form @submit.prevent="newsStore.submitComment(newsItem.id)" class="mt-3">
            <input class="form-control mb-2" type="text" v-model="newsStore.commentText" placeholder="Write a comment...">
            <button class="btn btn-info" type="submit">Submit</button>
          </form>
        </div>
      </div>
      </div>
    <div v-else class="alert alert-warning" role="alert">
        <p>Please log in to access this content.</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useNewsStore } from '../store/newsStore.ts';

export default defineComponent({
  setup() {
    const newsStore = useNewsStore();

    onMounted(async () => {
      console.log("Fetching user favorite category...");
      await newsStore.fetchUserData();
      console.log("Fetched user data:", newsStore.userData);

      console.log("Fetching news based on favorite category:", newsStore.userData.favorite_categories);
      await newsStore.fetchNews(newsStore.userData.favorite_categories);
      console.log("Fetched news:", newsStore.newsList);

      newsStore.checkAuthentication();
    });

    return { 
      newsStore,
      title: 'News',
    };
  },
});
</script>
