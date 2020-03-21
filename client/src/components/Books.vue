<template>
  <b-container>
    <b-row>
      <first></first>
    </b-row>
    <b-row>
      <b-col col sm="15">
        <h1>Books</h1>
        <hr>
        <br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Title</th>
            <th scope="col">Author</th>
            <th scope="col">Genre</th>
            <th scope="col">Year of writing</th>
            <th scope="col">Pages</th>
            <th scope="col">Publish house</th>
            <th></th>
          </tr>
          </thead>
          <tbody v-for="(book, index) in books" :key="index">
          <tr>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ book.genre }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.pages }}</td>
            <td>{{ book.publisher }}</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-warning btn-sm"
                  v-b-modal.book-update-modal
                  @click="editBook(book)">
                  Update
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="onDeleteBook(book)">
                  Delete
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </b-col>
    </b-row>
    <b-modal ref="addBookModal"
             id="book-modal"
             title="Add a new book"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                      label="Title:"
                      label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
          <b-form-input id="form-author-input"
                        type="text"
                        v-model="addBookForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-genre-group"
                      label="genre:"
                      label-for="form-genre-input">
          <b-form-input id="form-genre-input"
                        type="text"
                        v-model="addBookForm.genre"
                        required
                        placeholder="Enter genre">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-group"
                      label="Year:"
                      label-for="form-year-input">
          <b-form-input id="form-year-input"
                        type="text"
                        v-model="addBookForm.year"
                        required
                        placeholder="Enter year">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-pages-group"
                      label="Pages:"
                      label-for="form-pages-input">
          <b-form-input id="form-pages-input"
                        type="text"
                        v-model="addBookForm.pages"
                        required
                        placeholder="Enter pages">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-publisher-group"
                      label="Publisher:"
                      label-for="form-publisher-input">
          <b-form-input id="form-publisher-input"
                        type="text"
                        v-model="addBookForm.publisher"
                        required
                        placeholder="Enter publisher">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
             id="book-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-title-edit-group"
                      label="Title:"
                      label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editBookForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Author:"
                      label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editBookForm.author"
                        required
                        placeholder="Enter author">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-genre-edit-group"
                      label="genre:"
                      label-for="form-genre-edit-input">
          <b-form-input id="form-genre-edit-input"
                        type="text"
                        v-model="editBookForm.genre"
                        required
                        placeholder="Enter genre">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-year-edit-group"
                      label="Year:"
                      label-for="form-year-edit-input">
          <b-form-input id="form-year-edit-input"
                        type="text"
                        v-model="editBookForm.year"
                        required
                        placeholder="Enter year">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-pages-edit-group"
                      label="Pages:"
                      label-for="form-pages-edit-input">
          <b-form-input id="form-pages-edit-input"
                        type="text"
                        v-model="editBookForm.pages"
                        required
                        placeholder="Enter pages">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-publisher-edit-group"
                      label="Publisher:"
                      label-for="form-publisher-edit-input">
          <b-form-input id="form-publisher-edit-input"
                        type="text"
                        v-model="editBookForm.publisher"
                        required
                        placeholder="Enter publisher">
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </b-container>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import First from './Navigation.vue';

export default {
  data() {
    return {
      books: [],
      addBookForm: {
        title: '',
        author: '',
        genre: '',
        year: '',
        pages: '',
        publisher: '',
      },
      editBookForm: {
        id: '',
        title: '',
        author: '',
        genre: '',
        year: '',
        pages: '',
        publisher: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    first: First,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books/';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books/add/';
      axios.post(path, payload)
        .then((res) => {
          this.getBooks();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-отключение следующей строки
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.genre = '';
      this.addBookForm.year = '';
      this.addBookForm.pages = '';
      this.addBookForm.publisher = '';
      this.editBookForm.title = '';
      this.editBookForm.author = '';
      this.editBookForm.genre = '';
      this.editBookForm.year = '';
      this.editBookForm.pages = '';
      this.editBookForm.publisher = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        genre: this.addBookForm.genre,
        year: this.addBookForm.year,
        pages: this.addBookForm.pages,
        publisher: this.addBookForm.publisher,
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.editBookForm = book;
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}/edit/`;
      axios.put(path, payload)
        .then((res) => {
          this.getBooks();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editBookForm.title,
        author: this.editBookForm.author,
        genre: this.editBookForm.genre,
        year: this.editBookForm.year,
        pages: this.editBookForm.pages,
        publisher: this.editBookForm.publisher,
      };
      this.updateBook(payload, this.editBookForm.id);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}/delete/`;
      axios.delete(path)
        .then((res) => {
          this.getBooks();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
