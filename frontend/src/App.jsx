import { Input, Button, Select, ColorPicker } from "antd";
import axios from "axios";
import { useEffect, useState } from "react";

const hexToLightness = (hex) => {
  const value = hex.replace("#", "");
  if (value.length !== 6) {
    return 0;
  }

  const r = parseInt(value.slice(0, 2), 16) / 255;
  const g = parseInt(value.slice(2, 4), 16) / 255;
  const b = parseInt(value.slice(4, 6), 16) / 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  return ((max + min) / 2) * 100;
};

const getTileTextColor = (color) => {
  const parsedLightness = Number(color.lightness);
  const lightness = Number.isFinite(parsedLightness)
    ? parsedLightness
    : hexToLightness(color.hex);
  return lightness > 50 ? "#000000" : "#ffffff";
};

function App() {
  const [prompt, setPrompt] = useState("");
  const [paletteType, setPaletteType] = useState("subtle");
  const [numCols, setNumCols] = useState(3);
  const [response, setResponse] = useState(null);
  const [palette, setPalette] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.BACKEND_API_URL;

  useEffect(() => {
    if (response?.palette) {
      setPalette(response.palette);
    }
  }, [response]);

  const handleColorChange = (index, nextHex) => {
    setPalette((prevPalette) =>
      prevPalette.map((item, itemIndex) =>
        itemIndex === index
          ? { ...item, hex: nextHex, lightness: hexToLightness(nextHex) }
          : item,
      ),
    );
  };

  const search_prompt = async () => {
    setLoading(true);
    // console.log({
    //   prompt: prompt,
    //   palette_type: paletteType,
    //   num_colors: numCols,
    // });
    try {
      const res = await axios.post(`${API_URL}/generate-palette`, {
        prompt,
        palette_type: paletteType,
        num_colors: numCols,
      });

      setResponse(res.data);

      console.log(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full h-screen courier">
      <div className="h-[30vh] w-4/5 mx-auto">
        <h1 className="pt-6 text-3xl font-semibold flex gap-4 cursor-default">
          <div className="flex">
            <p className="transition-colors duration-100 ease-out hover:text-red-700">
              P
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-amber-500">
              r
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-sky-400">
              o
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-fuchsia-500">
              m
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-gray-800">
              p
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-blue-400">
              t
            </p>
          </div>
          <div className="flex">
            <p className="transition-colors duration-100 ease-out hover:text-pink-600">
              P
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-olive-600">
              a
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-green-600">
              l
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-teal-500">
              e
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-mauve-600">
              t
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-lime-400">
              t
            </p>
            <p className="transition-colors duration-100 ease-out hover:text-yellow-300">
              e
            </p>
          </div>
        </h1>
        <div className=" items-center pt-6 mx-auto  flex gap-10">
          <Input
            size="large"
            variant="outlined"
            placeholder="Enter prompt"
            value={prompt}
            className="h-fit"
            onChange={(e) => {
              setPrompt(e.target.value);
            }}
          />
          <Select
            className="w-36 h-fit"
            value={paletteType}
            onChange={setPaletteType}
            size="large"
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
            className="w-16 h-fit"
            defaultValue={3}
            value={numCols}
            onChange={setNumCols}
            size="large"
            options={[
              { value: 3, label: "3" },
              { value: 2, label: "2" },
              { value: 4, label: "4" },
              { value: 5, label: "5" },
              { value: 6, label: "6" },
            ]}
          />
          <Button
            className="h-fit"
            size="large"
            loading={loading}
            variant="solid"
            onClick={search_prompt}
          >
            Search
          </Button>
        </div>
      </div>
      <div className="w-full rounded-t-xl overflow-hidden  h-[70vh] ">
        <div className="h-full flex flex-nowrap">
          {palette.length > 0 &&
            palette.map((color, index) => (
              <div
                key={`${color.name}-${index}`}
                className="h-full min-w-0 flex-1"
                style={{ background: color.hex }}
              >
                <div
                  className="h-full flex flex-col items-center justify-center gap-2 px-3 text-center"
                  style={{ color: getTileTextColor(color) }}
                >
                  <ColorPicker
                    value={color.hex}
                    size="large"
                    showText
                    onChange={(value) =>
                      handleColorChange(index, value.toHexString())
                    }
                  />
                  <p className="text-base font-semibold">{color.hex}</p>
                  <p className="text-2xl font-semibold text-center wrap-break-word whitespace-normal">
                    {color.name}
                  </p>
                  <p>{color.role}</p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

export default App;
