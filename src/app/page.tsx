import Image from "next/image";

export default function Home() {
  return (
    <div className="container mx-auto p-4 sm:p-8 font-mono bg-gray-100 text-gray-800">
      <header className="text-center my-8">
        <h1 className="text-5xl font-bold text-red-600 tracking-wider">
          BOMB DEFUSAL MANUAL
        </h1>
        <p className="text-lg mt-2">
          For use by trained experts only. Read instructions carefully.
        </p>
        <p className="text-sm text-red-700 font-bold mt-1">
          Failure to comply may result in detonation.
        </p>
      </header>

      <main className="space-y-12">
        {/* Introduction Section */}
        <section id="introduction">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Introduction
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              You are the <span className="font-bold">Expert</span>. Your partner, the{" "}
              <span className="font-bold">Operator</span>, has a device with a
              ticking timer that must be disarmed. The Operator cannot see this
              manual, and you cannot see the device.
            </p>
            <p>
              You must communicate effectively to disarm all modules before the
              timer expires. This manual contains the instructions for each
              type of module that may appear on the device.
            </p>
          </div>
        </section>

        {/* Gyro-Stabilizer Module Section */}
        <section id="gyro">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Gyro-Stabilizer
          </h2>
          <div className="space-y-4">
            <p>
              This module is sensitive to movement. The Operator must keep the device oriented correctly to prevent a strike. The required orientation is determined by the color of the LED on the module.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Orientation Instructions:</h3>
              <ul className="list-disc list-inside space-y-1">
                <li><span className="font-bold">Green LED:</span> Keep the device perfectly level (screen facing up).</li>
                <li><span className="font-bold">Red LED:</span> Tilt the device 45 degrees forward.</li>
                <li><span className="font-bold">Blue LED:</span> Hold the device vertically (on its side).</li>
                <li><span className="font-bold">Yellow LED:</span> Keep the device upside down.</li>
              </ul>
              <p className="mt-4 text-sm text-red-700 font-bold">
                Warning: Any sudden movements or incorrect orientations will result in a strike. The module is disarmed once all other modules are solved.
              </p>
            </div>
          </div>
        </section>

        {/* Power Sequencer Module Section */}
        <section id="power-sequencer">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Power Sequencer
          </h2>
          <div className="space-y-4">
            <p>
              This module has four colored LEDs and four corresponding buttons. The LEDs will flash in a sequence. The Operator must describe the color sequence, and the Expert will provide the correct button press sequence.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Sequences:</h3>
              <p>Find the observed color sequence below to determine which buttons to press.</p>
              <table className="w-full mt-2 text-left border-collapse">
                <thead>
                  <tr>
                    <th className="border-b-2 border-gray-300 p-2">Color Sequence (First to Last)</th>
                    <th className="border-b-2 border-gray-300 p-2">Press Sequence</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Red → Blue → Green → Yellow</td>
                    <td className="p-2">Button 1, Button 3</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Yellow → Red → Blue → Green</td>
                    <td className="p-2">Button 4, Button 2, Button 1</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Blue → Green → Yellow → Red</td>
                    <td className="p-2">Button 2, Button 4</td>
                  </tr>
                   <tr className="border-b border-gray-200">
                    <td className="p-2">Green → Yellow → Red → Blue</td>
                    <td className="p-2">All Buttons</td>
                  </tr>
                   <tr>
                    <td className="p-2">Red → Red → Blue → Yellow</td>
                    <td className="p-2">Button 2, Button 2, Button 3</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>

      <footer className="text-center mt-12 py-4 border-t-2 border-gray-300">
        <p className="text-sm text-gray-600">
          Manual Version 1.0.0 | Property of Defusal Corp.
        </p>
      </footer>
    </div>
  );
}