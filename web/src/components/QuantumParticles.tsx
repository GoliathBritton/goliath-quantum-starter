'use client';

import React, { useRef, useMemo, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Points, PointMaterial, Sphere } from '@react-three/drei';
import * as THREE from 'three';

interface QuantumParticlesProps {
  count?: number;
  speed?: number;
  size?: number;
  opacity?: number;
  color?: string;
}

function QuantumField({ count = 2000, speed = 0.5, size = 0.8, opacity = 0.6, color = '#0ea5e9' }: QuantumParticlesProps) {
  const ref = useRef<THREE.Points>(null!);
  const { viewport } = useThree();
  
  // Generate random positions for particles
  const [positions, velocities] = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const velocities = new Float32Array(count * 3);
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      
      // Random positions within viewport
      positions[i3] = (Math.random() - 0.5) * viewport.width * 2;
      positions[i3 + 1] = (Math.random() - 0.5) * viewport.height * 2;
      positions[i3 + 2] = (Math.random() - 0.5) * 10;
      
      // Random velocities for quantum motion
      velocities[i3] = (Math.random() - 0.5) * speed * 0.02;
      velocities[i3 + 1] = (Math.random() - 0.5) * speed * 0.02;
      velocities[i3 + 2] = (Math.random() - 0.5) * speed * 0.01;
    }
    
    return [positions, velocities];
  }, [count, speed, viewport.width, viewport.height]);
  
  // Animate particles with quantum-like behavior
  useFrame((state) => {
    if (!ref.current) return;
    
    const time = state.clock.getElapsedTime();
    const positionArray = ref.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      
      // Update positions with quantum oscillation
      positionArray[i3] += velocities[i3] + Math.sin(time * 2 + i * 0.1) * 0.001;
      positionArray[i3 + 1] += velocities[i3 + 1] + Math.cos(time * 1.5 + i * 0.1) * 0.001;
      positionArray[i3 + 2] += velocities[i3 + 2] + Math.sin(time * 3 + i * 0.05) * 0.0005;
      
      // Wrap around boundaries
      if (positionArray[i3] > viewport.width) positionArray[i3] = -viewport.width;
      if (positionArray[i3] < -viewport.width) positionArray[i3] = viewport.width;
      if (positionArray[i3 + 1] > viewport.height) positionArray[i3 + 1] = -viewport.height;
      if (positionArray[i3 + 1] < -viewport.height) positionArray[i3 + 1] = viewport.height;
      if (positionArray[i3 + 2] > 5) positionArray[i3 + 2] = -5;
      if (positionArray[i3 + 2] < -5) positionArray[i3 + 2] = 5;
    }
    
    ref.current.geometry.attributes.position.needsUpdate = true;
    
    // Rotate the entire field slowly
    ref.current.rotation.x = Math.sin(time * 0.1) * 0.1;
    ref.current.rotation.y = Math.cos(time * 0.05) * 0.1;
  });
  
  return (
    <Points ref={ref} positions={positions} stride={3} frustumCulled={false}>
      <PointMaterial
        transparent
        color={color}
        size={size}
        sizeAttenuation={true}
        depthWrite={false}
        opacity={opacity}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
}

function QuantumConnections({ count = 100 }: { count?: number }) {
  const ref = useRef<THREE.LineSegments>(null!);
  const { viewport } = useThree();
  
  const [positions, connections] = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const connections: number[] = [];
    
    // Generate node positions
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      positions[i3] = (Math.random() - 0.5) * viewport.width * 1.5;
      positions[i3 + 1] = (Math.random() - 0.5) * viewport.height * 1.5;
      positions[i3 + 2] = (Math.random() - 0.5) * 8;
    }
    
    // Create connections between nearby nodes
    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        const dx = positions[i * 3] - positions[j * 3];
        const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
        const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
        const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
        
        if (distance < 3 && Math.random() > 0.7) {
          connections.push(i, j);
        }
      }
    }
    
    return [positions, connections];
  }, [count, viewport.width, viewport.height]);
  
  const linePositions = useMemo(() => {
    const linePos = new Float32Array(connections.length * 3);
    
    for (let i = 0; i < connections.length; i += 2) {
      const nodeA = connections[i];
      const nodeB = connections[i + 1];
      
      linePos[i * 3] = positions[nodeA * 3];
      linePos[i * 3 + 1] = positions[nodeA * 3 + 1];
      linePos[i * 3 + 2] = positions[nodeA * 3 + 2];
      
      linePos[(i + 1) * 3] = positions[nodeB * 3];
      linePos[(i + 1) * 3 + 1] = positions[nodeB * 3 + 1];
      linePos[(i + 1) * 3 + 2] = positions[nodeB * 3 + 2];
    }
    
    return linePos;
  }, [positions, connections]);
  
  useFrame((state) => {
    if (!ref.current) return;
    
    const time = state.clock.getElapsedTime();
    const material = ref.current.material as THREE.LineBasicMaterial;
    
    // Pulse the opacity
    material.opacity = 0.1 + Math.sin(time * 2) * 0.05;
  });
  
  return (
    <lineSegments ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={linePositions.length / 3}
          array={linePositions}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial
        color="#d946ef"
        transparent
        opacity={0.1}
        blending={THREE.AdditiveBlending}
      />
    </lineSegments>
  );
}

function QuantumOrbs() {
  const orbsRef = useRef<THREE.Group>(null!);
  
  useFrame((state) => {
    if (!orbsRef.current) return;
    
    const time = state.clock.getElapsedTime();
    
    orbsRef.current.children.forEach((orb, index) => {
      const sphere = orb as THREE.Mesh;
      const material = sphere.material as THREE.MeshBasicMaterial;
      
      // Floating motion
      sphere.position.y = Math.sin(time * 0.5 + index * 2) * 0.5;
      sphere.position.x = Math.cos(time * 0.3 + index * 1.5) * 2;
      
      // Pulsing glow
      material.opacity = 0.3 + Math.sin(time * 3 + index) * 0.2;
      
      // Rotation
      sphere.rotation.x += 0.01;
      sphere.rotation.y += 0.005;
    });
  });
  
  return (
    <group ref={orbsRef}>
      {[...Array(5)].map((_, i) => (
        <Sphere key={i} args={[0.2, 16, 16]} position={[i * 2 - 4, 0, -2]}>
          <meshBasicMaterial
            color={i % 2 === 0 ? '#0ea5e9' : '#d946ef'}
            transparent
            opacity={0.4}
            blending={THREE.AdditiveBlending}
          />
        </Sphere>
      ))}
    </group>
  );
}

export default function QuantumParticles({
  count = 1500,
  speed = 0.8,
  size = 1.2,
  opacity = 0.4,
  color = '#0ea5e9'
}: QuantumParticlesProps) {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 75 }}
        style={{ background: 'transparent' }}
        dpr={[1, 2]}
      >
        <QuantumField
          count={count}
          speed={speed}
          size={size}
          opacity={opacity}
          color={color}
        />
        <QuantumConnections count={80} />
        <QuantumOrbs />
        
        {/* Ambient lighting for subtle effects */}
        <ambientLight intensity={0.1} />
        <pointLight position={[10, 10, 10]} intensity={0.3} color="#0ea5e9" />
        <pointLight position={[-10, -10, -10]} intensity={0.3} color="#d946ef" />
      </Canvas>
    </div>
  );
}

// Quantum particle burst effect for interactions
export function QuantumBurst({ trigger, position }: { trigger: boolean; position: { x: number; y: number } }) {
  const burstRef = useRef<THREE.Points>(null!);
  const [isActive, setIsActive] = React.useState(false);
  
  useEffect(() => {
    if (trigger) {
      setIsActive(true);
      setTimeout(() => setIsActive(false), 1000);
    }
  }, [trigger]);
  
  const particles = useMemo(() => {
    const count = 50;
    const positions = new Float32Array(count * 3);
    const velocities = new Float32Array(count * 3);
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      const angle = (i / count) * Math.PI * 2;
      const radius = Math.random() * 0.5;
      
      positions[i3] = Math.cos(angle) * radius;
      positions[i3 + 1] = Math.sin(angle) * radius;
      positions[i3 + 2] = (Math.random() - 0.5) * 0.5;
      
      velocities[i3] = Math.cos(angle) * 0.1;
      velocities[i3 + 1] = Math.sin(angle) * 0.1;
      velocities[i3 + 2] = (Math.random() - 0.5) * 0.05;
    }
    
    return { positions, velocities };
  }, [trigger]);
  
  useFrame((state) => {
    if (!burstRef.current || !isActive) return;
    
    const time = state.clock.getElapsedTime();
    const positionArray = burstRef.current.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < 50; i++) {
      const i3 = i * 3;
      positionArray[i3] += particles.velocities[i3];
      positionArray[i3 + 1] += particles.velocities[i3 + 1];
      positionArray[i3 + 2] += particles.velocities[i3 + 2];
    }
    
    burstRef.current.geometry.attributes.position.needsUpdate = true;
  });
  
  if (!isActive) return null;
  
  return (
    <div className="fixed pointer-events-none" style={{ left: position.x, top: position.y, zIndex: 50 }}>
      <Canvas style={{ width: 200, height: 200, background: 'transparent' }}>
        <Points ref={burstRef} positions={particles.positions} stride={3}>
          <PointMaterial
            transparent
            color="#fbbf24"
            size={2}
            sizeAttenuation={true}
            depthWrite={false}
            opacity={0.8}
            blending={THREE.AdditiveBlending}
          />
        </Points>
      </Canvas>
    </div>
  );
}