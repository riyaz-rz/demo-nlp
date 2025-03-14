import React , {useState} from 'react';

const SearchBar = () => {

    const [input, setInput] = useState('');
    const [result, setResult] = useState('');
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/search', {
                method: 'GET',
            })

            const data = await response.text();
            alert(data)

        } catch (error) {
            console.log(error);
        }

        setResult(input)
    }

    return <div>
        <form onSubmit={handleSubmit}>
            <input type="text" 
            value = {input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your query" />
        </form>
        <div>
            <h3>Results</h3>
            <h1>
                {result}
                {/* <ul>
                    {result.map((result, index) => (
                        <li key={index}>{JSON.stringify(result)}</li>
                    ))}
                </ul> */}
            </h1>
        </div>


    </div>;
};

export default SearchBar;