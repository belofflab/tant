
import React, { useState } from 'react';
import ReactQuill, {Quill} from 'react-quill';
import 'react-quill/dist/quill.snow.css';



const Inline = Quill.import('blots/inline');
class BoldBlot extends Inline {}
BoldBlot.blotName = 'bold';
BoldBlot.tagName = 'b';
Quill.register('formats/bold', BoldBlot);



const formats = ['bold', 'italic', 'underline', 'strike', 'link'];
const modules = {
    toolbar: [
      ['bold', 'italic', 'underline','strike'],
      ['link'],
      ['clean']
    ],
    keyboard: {
      bindings: {
        enter: {
          key: 13,
          handler: () => {
            console.log("123")
          }
        }
      }
    }
}

export default function RichInput({setData}) {
  const handleChange = (value) => {
    setData(value.replaceAll(/<\/?p[^>]*>/g, '').replaceAll(/<\/?span[^>]*>/g, '').replaceAll('<br>', '\n'));
  };

  return <ReactQuill theme="snow"  formats={formats} modules={modules} onChange={handleChange} />;
}