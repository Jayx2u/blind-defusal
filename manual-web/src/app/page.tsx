// import Image from "next/image";

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
              type of module and type of identifiable features that may appear on the device.
            </p>
          </div>
        </section>

        {/* On the Subject of the Bomb Section */}
        <section id="on-the-bomb">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            On the Subject of the Bomb
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              A bomb will have one or more modules that must be disarmed. Each module is self-contained and can be disarmed in any order. Instructions for each module are below.
            </p>
            <p>
              Some disarming instructions will require information from the bomb itself, such as the serial number or batteries. This information can be found on the sides of the bomb casing.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Timer and Strikes</h3>
              <ul className="list-disc list-inside space-y-2">
                <li>The bomb has a countdown timer. When it reaches 0:00, it will explode.</li>
                <li>
                  If a mistake is made, the bomb will record a strike and the timer will speed up. A small LED above the timer will light for each strike.
                </li>
                <li>
                  If you receive <span className="font-bold text-red-700">three strikes</span>, the bomb will explode.
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Identification: Serial Number Section */}
        <section id="serial-number">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Identification: Serial Number
          </h2>
          <div className="space-y-4 text-lg">
            <p>
              The bomb&apos;s serial number is crucial for disarming certain modules. It can be found on the side of the bomb casing.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Serial Number Format</h3>
              <p>
                The serial number consists of a combination of letters and numbers. For example: <span className="font-bold p-1 bg-gray-200 rounded">SN48K2</span>.
              </p>
              <p className="mt-2">
                Pay close attention to specific digits or letters when requested by a module&apos;s instructions, especially whether a digit is <span className="font-bold">odd or even</span>.
              </p>
            </div>
          </div>
        </section>

        {/* Gyro-Stabilizer Module Section */}
        <section id="gyro">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Needy Module: Gyro-Stabilizer
          </h2>
          <div className="space-y-4">
            <p>
              This is a <span className="font-bold">needy module</span> that requires constant supervision. It is sensitive to movement and will check its orientation at random intervals. The Operator must keep the device oriented correctly to prevent a strike. The required orientation is determined by the color of the LED on the module.
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
              This module has four colored LEDs and four corresponding buttons. The LEDs will flash in a sequence. The Operator must describe the color sequence, and the Expert will provide the correct button press sequence, which may depend on the bomb&apos;s serial number.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white">
              <h3 className="text-xl font-bold mb-2">Conditional Sequences:</h3>
              <p>Find the observed color sequence below and follow the condition to determine which buttons to press.</p>
              <table className="w-full mt-2 text-left border-collapse">
                <thead>
                  <tr>
                    <th className="border-b-2 border-gray-300 p-2">Color Sequence</th>
                    <th className="border-b-2 border-gray-300 p-2">Condition</th>
                    <th className="border-b-2 border-gray-300 p-2">Press Sequence</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-200">
                    <td className="p-2" rowSpan={2}>Red → Blue → Green → Yellow</td>
                    <td className="p-2">If last digit of serial is even...</td>
                    <td className="p-2">Button 1, Button 3</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 2, Button 4</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2" rowSpan={2}>Yellow → Red → Blue → Green</td>
                    <td className="p-2">If serial has a vowel...</td>
                    <td className="p-2">Button 4, Button 2, Button 1</td>
                  </tr>
                   <tr className="border-b border-gray-200">
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 3, Button 1</td>
                  </tr>
                  <tr className="border-b border-gray-200">
                    <td className="p-2">Blue → Green → Yellow → Red</td>
                    <td className="p-2">Always...</td>
                    <td className="p-2">Button 2, Button 4</td>
                  </tr>
                   <tr className="border-b border-gray-200">
                    <td className="p-2">Green → Yellow → Red → Blue</td>
                    <td className="p-2">Always...</td>
                    <td className="p-2">All Buttons</td>
                  </tr>
                   <tr>
                    <td className="p-2" rowSpan={2}>Red → Red → Blue → Yellow</td>
                    <td className="p-2">If last digit of serial is odd...</td>
                    <td className="p-2">Button 2, Button 2, Button 3</td>
                  </tr>
                  <tr>
                    <td className="p-2">Otherwise...</td>
                    <td className="p-2">Button 1, Button 4</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Wire Pulling Module Section */}
        <section id="wire-pulling">
          <h2 className="text-3xl font-bold border-b-4 border-gray-700 pb-2 mb-4">
            Module: Wire Pulling
          </h2>
          <div className="space-y-4">
            <p>
              This module presents 3 to 6 colored wires running vertically. To disarm it, one specific wire must be carefully pulled from its socket. Pulling the wrong wire will cause a strike. The wires must not be cut.
            </p>
            <div className="p-4 border-2 border-gray-400 rounded-lg bg-white space-y-4">
              <div>
                <h3 className="text-xl font-bold">If there are 3 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there are no red wires, pull the second wire.</li>
                  <li>Otherwise, if the last wire is white, pull the last wire.</li>
                  <li>Otherwise, if there is more than one blue wire, pull the last blue wire.</li>
                  <li>Otherwise, pull the last wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 4 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there is more than one red wire and the last digit of the serial number is odd, pull the last red wire.</li>
                  <li>Otherwise, if the last wire is yellow and there are no red wires, pull the first wire.</li>
                  <li>Otherwise, if there is exactly one blue wire, pull the first wire.</li>
                  <li>Otherwise, pull the second wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 5 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If the last wire is black and the last digit of the serial number is odd, pull the fourth wire.</li>
                  <li>Otherwise, if there is exactly one red wire and more than one yellow wire, pull the first wire.</li>
                  <li>Otherwise, if there are no black wires, pull the second wire.</li>
                  <li>Otherwise, pull the first wire.</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-bold">If there are 6 wires:</h3>
                <ul className="list-disc list-inside mt-1">
                  <li>If there are no yellow wires and the last digit of the serial number is odd, pull the third wire.</li>
                  <li>Otherwise, if there is exactly one yellow wire and more than one white wire, pull the fourth wire.</li>
                  <li>Otherwise, if there are no red wires, pull the last wire.</li>
                  <li>Otherwise, pull the fourth wire.</li>
                </ul>
              </div>
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