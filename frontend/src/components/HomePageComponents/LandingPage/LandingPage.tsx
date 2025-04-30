// import { useRef, useEffect, useState, Suspense } from "react";
// import { Canvas, useFrame } from "@react-three/fiber";
// import { useGLTF, OrbitControls } from "@react-three/drei";
// import * as THREE from "three";
// import style from "./landing.module.css";

// // Definizione dell'interfaccia per i tipi
// interface ModelProps {
//   url: string;
//   position: [number, number, number];
// }

// // Componente per il modello 3D
// function Model({ url, position }: ModelProps) {
//   const { scene, animations } = useGLTF(url);
//   const modelRef = useRef<THREE.Group>(null);
//   const mixerRef = useRef<THREE.AnimationMixer | null>(null);

//   // Inizializza l'animation mixer quando il modello viene caricato
//   useEffect(() => {
//     if (modelRef.current && animations.length) {
//       const mixer = new THREE.AnimationMixer(modelRef.current);
//       animations.forEach((clip) => {
//         const action = mixer.clipAction(clip);
//         action.play();
//       });
//       mixerRef.current = mixer;
//     }
//   }, [animations]);

//   // Aggiorna le animazioni ad ogni frame
//   useFrame((state, delta) => {
//     if (mixerRef.current) {
//       mixerRef.current.update(delta);
//     }
//   });

//   return (
//     <group ref={modelRef} scale={[1, 1, 1]} position={position}>
//       <primitive object={scene} />
//     </group>
//   );
// }

// // Componente per la scena 3D
// function Scene({ modelPosition }: { modelPosition: [number, number, number] }) {
//   // Percorso per il file nella cartella public
//   const modelUrl: string = "/assets/3DModels/kuma_heavy_robot_r-9000s.glb";

//   return (
//     <>
//       <ambientLight intensity={0.8} />
//       <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1.2} />
//       <directionalLight position={[-5, 5, 5]} intensity={0.8} />
//       <Suspense fallback={null}>
//         <Model url={modelUrl} position={modelPosition} />
//       </Suspense>
//       <OrbitControls 
//         enableZoom={false} 
//         enablePan={false}
//       />
//     </>
//   );
// }

// const LandingPage: React.FC = () => {
//   // Aggiungi stato per la larghezza della finestra
//   const [windowWidth, setWindowWidth] = useState<number>(
//     typeof window !== 'undefined' ? window.innerWidth : 1920
//   );

//   // Aggiungi listener per il ridimensionamento
//   useEffect(() => {
//     const handleResize = () => {
//       setWindowWidth(window.innerWidth);
//     };

//     window.addEventListener("resize", handleResize);
//     return () => window.removeEventListener("resize", handleResize);
//   }, []);

//   // Calcola la posizione del modello in base alla larghezza della finestra
//   let modelPosition: [number, number, number] = [4000, 700, 100];

//   if (windowWidth < 1000) {
//     modelPosition = [3000, 700, 100];
//   } else if (windowWidth < 600) {
//     modelPosition = [2000, 700, 100];
//   }

//   return (
//     <div className="relative flex flex-col items-center justify-center bg-transparent text-text-color p-4 h-screen">
//       {/* Canvas di Three.js come background */}
//       <div className="absolute inset-0 z-0">
//         <Canvas
//           camera={{
//             position: [0, 0, 5000],
//             fov: 50,
//             near: 0.1, 
//             far: 10000,
//           }}
//           style={{ width: "100%", height: "100%", background: "transparent" }}
//         >
//           <Suspense fallback={null}>
//             <Scene modelPosition={modelPosition} />
//           </Suspense>
//         </Canvas>
//       </div>

//       {/* Contenuto in primo piano */}
//       <div className="relative z-10">
//         <h1 className="text-3xl font-bold">Welcome to RoboLab</h1>
//       </div>
//     </div>
//   );
// };

// export default LandingPage;

import { useRef, useEffect, Suspense } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF, OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import style from "./landing.module.css";

// Definizione dell'interfaccia per i tipi
interface ModelProps {
  url: string;
}

// Componente per il modello 3D
function Model({ url }: ModelProps) {
  const { scene, animations } = useGLTF(url);
  const modelRef = useRef<THREE.Group>(null);
  const mixerRef = useRef<THREE.AnimationMixer | null>(null);

  // Inizializza l'animation mixer quando il modello viene caricato
  useEffect(() => {
    if (modelRef.current && animations.length) {
      const mixer = new THREE.AnimationMixer(modelRef.current);
      animations.forEach((clip) => {
        const action = mixer.clipAction(clip);
        action.play();
      });
      mixerRef.current = mixer;
    }
  }, [animations]);

  // Aggiorna le animazioni ad ogni frame
  useFrame((state, delta) => {
    if (mixerRef.current) {
      mixerRef.current.update(delta);
    }
  });

  return (
    <group ref={modelRef} scale={[1, 1, 1]} position={[1500, 1000, 0]}>
      <primitive object={scene} />
    </group>
  );
}

// Componente per la scena 3D
function Scene() {
  // Percorso per il file nella cartella public
  const modelUrl: string = "/assets/3DModels/kuma_heavy_robot_r-9000s.glb";

  return (
    <>
      <ambientLight intensity={0.8} />
      <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1.2} />
      <directionalLight position={[-5, 5, 5]} intensity={0.8} />
      <Suspense fallback={null}>
        <Model url={modelUrl} />
      </Suspense>
      <OrbitControls 
        enableZoom={false} 
        enablePan={false}
      />
    </>
  );
}

const LandingPage: React.FC = () => {
  return (
    <div className="flex flex-col md:flex-row h-screen w-full">
      {/* Sezione contenuto (70%) */}
      <div className="w-full md:w-[65%] flex flex-col justify-center items-center p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to RoboLab</h1>
        <p className="text-xl">This is the landing page.</p>
        {/* Puoi aggiungere più contenuto qui */}
      </div>

      {/* Sezione modello 3D (30%) */}
      <div className="w-full md:w-[35%] h-full relative">
        <Canvas
          camera={{
            position: [0, 0, 6000],
            fov: 50,
            near: 0.1, 
            far: 10000,
          }}
          style={{ width: "100%", height: "100%" }}
        >
          <Suspense fallback={null}>
            <Scene />
          </Suspense>
        </Canvas>
      </div>
    </div>
  );
};

export default LandingPage;
