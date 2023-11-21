<template>
  <div class="container mt-4">
    <h3 class="mb-3">{{ title }}</h3>
    <div v-for="newsItem in newsList" :key="newsItem.id" class="mb-5">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">{{ newsItem.title }}</h4>
          <p class="card-text">{{ newsItem.text }}</p>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="mt-4">
        <h5>Comments</h5>
        <div v-for="comment in newsItem.comments" :key="comment.id" class="card mb-2">
          <div class="card-body">
            <p><strong>{{ comment.author_email }}:</strong> {{ comment.text }}</p>
            <button class="btn btn-sm btn-outline-primary" @click="startReply(comment.id, comment.author_email)">Reply</button>

            <!-- Display Replies with Indentation -->
            <div v-for="reply in comment.replies" :key="reply.id" class="ml-4 mt-2 card bg-light">
              <div class="card-body">
                <p>
                  <strong>{{ reply.author_email }}</strong> replying to <strong>{{ comment.author_email }}:</strong>
                  {{ reply.text }}
                </p>
              </div>
            </div>

            <!-- Reply Form -->
            <div v-if="replyingTo === comment.id" class="mt-2">
              <input class="form-control mb-2" type="text" v-model="commentText" placeholder="Replying to {{ replyingToEmail }}...">
              <button class="btn btn-sm btn-success" @click="submitReply(newsItem.id)">Submit Reply</button>
            </div>
          </div>
        </div>

        <!-- Form to submit a new top-level comment -->
        <form @submit.prevent="submitComment(newsItem.id)" class="mt-3">
          <input class="form-control mb-2" type="text" v-model="commentText" placeholder="Write a comment...">
          <button class="btn btn-info" type="submit">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>



<script lang="ts">
import { defineComponent } from "vue";

interface Comment {
  id: number;
  author_email: string;
  text: string;
  replies: Comment[];
}

interface NewsItem {
  id: number;
  title: string;
  text: string;
  comments: Comment[];
}

export default defineComponent({
    data() {
        return {
            title: "News",
            newsList: [] as NewsItem[],
            userData: {
              email: '',
              date_of_birth: '',
              profile_image: '',
              favorite_category: ''
            },
            commentText: '',
            replyingTo: null as number | null,  // ID of the comment being replied to
            replyingToEmail: null as string | null, // Email of the user being replied to
        }
    },
    created() {
        this.fetchUserFavoriteCategory(); // Fetch the user's favorite category on component creation // Then fetch news based on that category
    },
    methods: {
        async fetchUserFavoriteCategory() {
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

              } else {
                // User is authenticated
                console.log(data);
                this.userData = data;
                this.fetchNews();
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
        async fetchNews() {
            if (!this.userData.favorite_category) return; // Don't fetch if the category is not set

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/news/${this.userData.favorite_category}/`, {
                    method: 'GET',
                    credentials: 'include',
                });
                if (response.ok) {
                    const newsList = await response.json();
                    for (let newsItem of newsList) {
                        await this.fetchCommentsForNewsItem(newsItem);
                    }
                    this.newsList = newsList;
                } else {
                    console.error('Failed to fetch news');
                }
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        },
        async fetchCommentsForNewsItem(newsItem: { id: any; comments: any; }) {
            try {
                const commentResponse = await fetch(`http://127.0.0.1:8000/api/news/${newsItem.id}/comments/`, {
                    method: 'GET',
                    credentials: 'include',
                });
                if (commentResponse.ok) {
                    newsItem.comments = await commentResponse.json();
                } else {
                    console.error('Failed to fetch comments for news item:', newsItem.id);
                }
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        },
        async submitComment(newsItemId: number) {
          if (!this.commentText.trim()) return; // Do nothing if the comment is empty

          try {
              const response = await fetch(`http://127.0.0.1:8000/api/news/${newsItemId}/submit-comment/`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      // Add any other necessary headers, like Authorization if needed
                  },
                  body: JSON.stringify({ text: this.commentText }),
                  credentials: 'include',
              });

              if (response.ok) {
                  console.log('Comment submitted successfully');
                  this.commentText = ''; // Clear the comment input field
                  this.fetchNews(); // Refetch news to update the list with the new comment
              } else {
                  console.error('Failed to submit comment:', response.status, response.statusText);
              }
          } catch (error) {
              console.error('Error submitting comment:', error);
          }
      },
      startReply(commentId: number | null, authorEmail: string) {
          this.replyingTo = commentId;
          this.replyingToEmail = authorEmail; // Store the email of the user being replied to
          this.commentText = ''; // Reset the comment text
      },
      async submitReply(newsItemId: number) {
            if (!this.commentText.trim()) return; // Do nothing if the comment is empty

            try {
                const response = await fetch(`http://127.0.0.1:8000/api/news/${newsItemId}/submit-comment/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: this.commentText,
                        parent_id: this.replyingTo // Include the parent ID
                    }),
                    credentials: 'include',
                });

                if (response.ok) {
                    console.log('Reply submitted successfully');
                    this.commentText = ''; // Clear the comment input field
                    this.replyingTo = null; // Reset the replyingTo ID
                    this.fetchNews(); // Refetch news to update the list with the new reply
                } else {
                    console.error('Failed to submit reply:', response.status, response.statusText);
                }
            } catch (error) {
                console.error('Error submitting reply:', error);
            }
        }
    }
})
</script>
