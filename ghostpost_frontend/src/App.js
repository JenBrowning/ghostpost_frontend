import React, { Component } from "react";
import axios from "axios";
import './App.css';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = { posts: [] };
  }
  componentDidMount() {
    this.apiGetRequest("http://127.0.0.1:8000/boastroast/");
  }
  apiGetRequest = url => {
    axios
      .get(url)
      .then(res => {
        this.setState({
          posts: res.data
        });
      })
      .catch(err => console.log(err));
    return this.state.posts;
  };

  handleChange = event => {
    event.preventDefault();
    const data = {
      [event.target.name]: event.target.value
    };
    this.setState({
      posts: data
    });
    console.log(this.state.posts);
  };

  apiPostRequest = () => {
    let newID = Math.max(this.state.posts.id) + 1;
    axios
      .post("http://127.0.0.1:8000/boastroast/" + newID, this.state.posts)
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
      .catch(err => console.log(err));
  };

  sortPosts = (a, b) => {
    const posts_array = this.state.posts;
    posts_array.sort(function(vote1, vote2) {
      if (vote1.vote > vote2.vote) return a;
      if (vote1.vote < vote2.vote) return b;
    });
    this.setState({ posts: posts_array });
    return this.state.posts;
  };

  changeVote = (data, event) => {
    console.log(event.target.value, data);
  };

  render() {
    return (
      <React.Fragment>
        <Navbar apiGetRequest={this.apiGetRequest} sortPosts={this.sortPosts} />
        <Comments posts={this.state.posts} changeVote={this.changeVote} />
        <NewPost
          apiPostRequest={this.apiPostRequest}
          handleChange={this.handleChange}
        />
      </React.Fragment>
    );
  }
}

class NewPost extends Component {
  render() {
    return (
      <div className="main">
        <form onSubmit={this.props.apiPostRequest}>
          Choose Boast or Roast:
          <select name="title">
            <option value="b">Boast</option>
            <option value="r">Roast</option>
          </select>
          <br />
          <br />
          <br />
          Comment:
          <input name="comment" type="text" />
          <br />
          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}

class Navbar extends Component {
  render() {
    return (
      <div className="navbar">
        <button
          onClick={() =>
            this.props.apiGetRequest("http://127.0.0.1:8000/boastroast/")
          }
        >
          All Posts
        </button>
        <button
          onClick={() =>
            this.props.apiGetRequest("http://127.0.0.1:8000/roast/")
          }
        >
          Roasts
        </button>
        <button
          onClick={() =>
            this.props.apiGetRequest("http://127.0.0.1:8000/boast/")
          }
        >
          Boasts
        </button>
        <button onClick={() => this.props.sortPosts(-1, 1)}>
          Upvoted Posts
        </button>
        <button onClick={() => this.props.sortPosts(1, -1)}>Downvoted Posts</button>
      </div>
    );
  }
}

class Comments extends Component {
  render() {
    return (
      <div>
        <ul>
          {this.props.posts.map((post, index) => (
            <div id="post" key={index}>
              <h3>{post.title === "b" ? "Boast" : "Roast"}</h3>
              <li>" {post.comment} "</li>
              <li>votes: {post.vote}</li>
              <li>{post.id}</li>
              <button onClick={() => this.props.changeVote()}>Downvote</button>
              <button onClick={() => this.props.changeVote()}>Upvote</button>
            </div>
          ))}
        </ul>
      </div>
    );
  }
}

export default App;





