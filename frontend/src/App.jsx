import { Input, Button, Row, Col, Select } from "antd";
import axios from "axios";
import { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [paletteType, setPaletteType] = useState("subtle");
  const [numCols, setNumCols] = useState(3);
  const [response, setResponse] = useState(null);
  const search_prompt = async () => {
    console.log({
      prompt: prompt,
      palette_type: paletteType,
      num_colors: numCols,
    });
    try {
      const res = await axios.post("http://127.0.0.1:8000/generate-palette", {
        prompt: prompt,
        palette_type: paletteType,
        num_colors: numCols,
      });
      setResponse(res.data);
      console.log(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="w-full h-screen ">
      <div className="w-4/5 mx-auto pt-24 flex gap-10">
        <Input
          size="large"
          variant="outlined"
          placeholder="Enter prompt"
          value={prompt}
          onChange={(e) => {
            setPrompt(e.target.value);
          }}
        />
        <Select
          className="w-36"
          value={paletteType}
          onChange={setPaletteType}
          defaultValue={"subtle"}
          options={[
            { value: "subtle", label: "Subtle" },
            { value: "monochrome", label: "monochrome" },
            { value: "complementary", label: "complementary" },
            { value: "analogous", label: "analogous" },
            { value: "vibrant", label: "vibrant" },
            { value: "triadic", label: "triadic" },
          ]}
        />
        <Select
          className="w-16"
          defaultValue={3}
          value={numCols}
          onChange={setNumCols}
          options={[
            { value: 3, label: "3" },
            { value: 2, label: "2" },
            { value: 4, label: "4" },
            { value: 5, label: "5" },
            { value: 6, label: "6" },
          ]}
        />
        <Button size="large" variant="solid" onClick={search_prompt}>
          Search
        </Button>
      </div>
      <div className="w-4/5 mx-auto pt-8">
        <Row className="h-12">
          <Col
            span={6}
            className="  text-center flex items-center justify-center"
          >
            HEX
          </Col>
          <Col
            span={6}
            className=" text-center flex items-center justify-center"
          >
            Score 1
          </Col>
          <Col
            span={6}
            className=" text-center flex items-center justify-center"
          >
            Score 2
          </Col>
          <Col
            span={6}
            className=" text-center flex items-center justify-center"
          >
            Score 3
          </Col>
        </Row>
        {response &&
          response.palette.map((color) => (
            <Row key={color.hex} className="h-12">
              <Col span={6} style={{ background: color.hex }}>
                {color.hex}
              </Col>
              <Col
                span={6}
                className=" text-center flex items-center justify-center"
              >
                {color.name}
              </Col>
              <Col
                span={6}
                className=" text-center flex items-center justify-center"
              >
                {color.role}
              </Col>
              <Col
                span={6}
                className=" text-center flex items-center justify-center"
              >
                {color.hue}
                {color.saturation}
                {color.lightness}
              </Col>
            </Row>
          ))}
      </div>
    </div>
  );
}

export default App;
