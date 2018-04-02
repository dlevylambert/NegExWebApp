import React from 'react';
import axios from 'axios';

class FileUpload extends React.Component {
  constructor(props) {
    super(props);
    this.state ={
      file:null,
      fileContents:null
    }
    this.onFormSubmit = this.onFormSubmit.bind(this)
    this.onChange = this.onChange.bind(this)
    this.fileUpload = this.fileUpload.bind(this)
  }
  onFormSubmit(event){
    event.preventDefault()
    this.fileUpload(this.state.file).then((response)=>{
    	this.setState({fileContents: response.data})
    })
  }
  onChange(event) {
    this.setState({file:event.target.files[0]})
  }
  fileUpload(file){
    var formData = new FormData();
		formData.append('file', file);
		return axios.post('/upload_file', formData, {
		  headers: {'content-type': 'multipart/form-data'}
		});
  }

  render() {
  	var encodedUri = encodeURI(this.state.fileContents);
  	var href = 'data:application/octet-stream,' + encodedUri
    return (
    	<div>
        <p>Create a csv file using the following template and upload it to find all incidences of your diagnosis of interest</p>
	      <form onSubmit={this.onFormSubmit}>
	        <input type='file' onChange={this.onChange} />
	        {this.state.file && <button type='submit'>Upload</button>}
	      </form>
	      {this.state.fileContents && <a href={href} className="btn btn-success" download="my_data.csv">Download Results</a>}
	    </div>
   )
  }
};

export default FileUpload;
