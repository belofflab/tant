import React, { useState, useEffect } from 'react';
import RichInput from '../../components/RichInput';



export default function Home() {

    const [text, setText] = useState(null);

    const show =() => {
        console.log(text)
    }

  return <>
  <button onClick={show}>Show</button>
    <RichInput setData={setText} />
  </>;
}