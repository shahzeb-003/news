// src/store/newsStore.js
import { defineStore } from 'pinia';

interface NewsItem {
  id: number;
  title: string;
  text: string;
  comments: Comment[];
  // Add other properties as needed
}

interface Comment {
  id: number;
  author_email: string;
  text: string;
  replies: Comment[];
  // Add other properties as needed
}

interface UserData {
  email: string;
  date_of_birth: string;
  profile_image: string;
  favorite_categories: string[]; // Changed to an array
}

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [] as NewsItem[],
    userData: {} as UserData,
    commentText: '',
    replyingTo: null as number | null,
    replyingToEmail: null as string | null,
    editingCommentId: null as number | null,
    editedCommentText: '',
    isAuthenticated: false,
    selectedFile: null as File | null,
  }),

  actions: {
    async fetchUserData() {
      try {
        const response = await fetch(`http://localhost:8000/api/user-details/`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.userData = data;
        } else {
          console.error('User is not authenticated');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    async fetchNews(favoriteCategories: string[]) {
      if (!favoriteCategories || favoriteCategories.length === 0) return;
    
      let allNews: any[] = [];
    
      try {
        for (const category of favoriteCategories) {
          const response = await fetch(`http://localhost:8000/api/news/${category}`, {
            method: 'GET',
            credentials: 'include',
          });
    
          if (response.ok) {
            const newsList = await response.json();
            for (let newsItem of newsList) {
              await this.fetchCommentsForNewsItem(newsItem);
            }
            allNews = allNews.concat(newsList);
          } else {
            console.error(`Failed to fetch news for category ${category}`);
          }
        }
    
        this.newsList = allNews;
      } catch (error) {
        console.error('Error fetching news:', error);
      }
    },
    async fetchCommentsForNewsItem(newsItem: { id: any; comments: any; }) {
      try {
        const commentResponse = await fetch(`http://localhost:8000/api/news/${newsItem.id}/comments/`, {
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
    async submitComment(newsItemId: any) {
        if (!this.commentText.trim()) return;
  
        try {
          const response = await fetch(`http://localhost:8000/api/news/${newsItemId}/submit-comment/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: this.commentText }),
            credentials: 'include',
          });
  
          if (response.ok) {
            console.log('Comment submitted successfully');
            this.commentText = '';
            await this.fetchNews(this.userData.favorite_categories);
          } else {
            console.error('Failed to submit comment:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Error submitting comment:', error);
        }
      },

      startReply(commentId: number, authorEmail: string) {
        this.replyingTo = commentId;
        this.replyingToEmail = authorEmail;
        this.commentText = '';
      },
      async submitReply(newsItemId: any) {
        if (!this.commentText.trim()) return;
  
        try {
          const response = await fetch(`http://localhost:8000/api/news/${newsItemId}/submit-comment/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              text: this.commentText,
              parent_id: this.replyingTo,
            }),
            credentials: 'include',
          });
  
          if (response.ok) {
            console.log('Reply submitted successfully');
            this.commentText = '';
            this.replyingTo = null;
            await this.fetchNews(this.userData.favorite_categories);
          } else {
            console.error('Failed to submit reply:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Error submitting reply:', error);
        }
      },
  
      startEditing(comment: { id: number; text: string; }) {
        this.editingCommentId = comment.id;
        this.editedCommentText = comment.text;
      },
  
      async submitEdit(commentId: any) {
        try {
          const response = await fetch(`http://localhost:8000/api/edit-comment/${commentId}/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: this.editedCommentText }),
            credentials: 'include',
          });
  
          if (response.ok) {
            console.log('Comment edited successfully');
            this.editingCommentId = null;
            this.editedCommentText = '';
            await this.fetchNews(this.userData.favorite_categories);
          } else {
            console.error('Failed to edit comment:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Error editing comment:', error);
        }
      },
  
      cancelEditing() {
        this.editingCommentId = null;
        this.editedCommentText = '';
      },
  
      async deleteComment(commentId: any) {
        if (!confirm("Are you sure you want to delete this comment?")) return;
  
        try {
          const response = await fetch(`http://localhost:8000/api/delete-comment/${commentId}/`, {
            method: 'DELETE',
            headers: {
              // Include necessary headers
            },
            credentials: 'include',
          });
  
          if (response.ok) {
            console.log('Comment deleted successfully');
            await this.fetchNews(this.userData.favorite_categories);
          } else {
            console.error('Failed to delete comment:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Error deleting comment:', error);
        }
      },




      async logout() {
        try {
          const response = await fetch('http://localhost:8000/api/logout/', {
            method: 'POST',
            credentials: 'include', // Use 'include' to send cookies
          });
  
          if (response.ok) {
            window.location.href = 'http://localhost:8000/login/';
          } else {
            // Handle logout failure
            console.error('Logout failed:', response.status, response.statusText);
          }
        } catch (error) {
          console.error('Logout failed:', error);
          // Handle logout failure
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
        this.userData.favorite_categories.forEach(category => {
          formData.append('favorite_categories', category);
        });
        
        if (this.selectedFile) {
          formData.append('profile_image', this.selectedFile, this.selectedFile.name);
        }
  
        try {
          const response = await fetch('http://localhost:8000/api/update-user-details/', {
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
      profileImageUrl() {
        if(!this.userData.profile_image) return

        return `http://localhost:8000${this.userData.profile_image}`;
      },
      async checkAuthentication() {
        try {
          const response = await fetch('http://localhost:8000/api/check-authentication/', {
            credentials: 'include'
          });
          this.isAuthenticated = response.ok;
        } catch (error) {
          console.error('Error checking authentication:', error);
          this.isAuthenticated = false;
        }
      },

    }


    // Add methods for submitting, editing, and deleting comments
    // Each method should update the state and perform the necessary API calls
  
});
